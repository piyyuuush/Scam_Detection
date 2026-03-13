import streamlit as st
import zipfile
import os
import time

# --- Custom CSS ---
st.markdown("""
    <style>
        body, [class*="stApp"] {
            background-color: #000000 !important;
            color: #00ffcc !important;
            font-family: 'Courier New', monospace;
        }

        .card {
            background-color: #0d0d0d;
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 0 20px #00ffcc55;
            margin-top: 20px;
            border: 1px solid #00ffcc55;
        }

        .red-label {
            color: #ff4d6d;
            font-weight: bold;
            font-size: 18px;
            text-shadow: 0 0 10px #ff4d6d;
        }

        .threat-box {
            background: linear-gradient(90deg, #ff1a1a, #ff4d6d);
            color: #fff;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-weight: bold;
            font-size: 18px;
            text-align: center;
            box-shadow: 0 0 25px #ff4d6d;
            animation: blink 1s infinite alternate;
        }

        .flags-box {
            background-color: #1a1a1a;
            color: #ffcc00;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 15px;
            border: 1px solid #ffcc00;
            box-shadow: 0 0 15px #ffcc00;
        }

        .solution-box {
            background-color: #1a1a1a;
            color: #00ffcc;
            padding: 15px;
            border-radius: 10px;
            margin-top: 15px;
            font-size: 15px;
            border: 1px solid #00ffcc;
            box-shadow: 0 0 15px #00ffcc;
        }

        @keyframes blink {
            from { opacity: 1; }
            to { opacity: 0.6; }
        }
    </style>
""", unsafe_allow_html=True)


def scan_zip(file_path: str):
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            files = z.namelist()

        suspicious = [f for f in files if f.endswith((".exe", ".bat", ".cmd", ".scr"))]

        if suspicious:
            return {
                "safe": False,
                "threat": "⚠ Suspicious Files Found",
                "flags": suspicious,
                "solution": [
                    "❌ Do NOT extract unknown ZIP files",
                    "❌ Never run EXE/BAT files from email ZIPs",
                    "✅ Scan ZIP with antivirus"
                ]
            }

        return {
            "safe": True,
            "threat": "✔ No Threat Detected",
            "flags": [],
            "solution": ["ZIP looks safe ✅"]
        }

    except Exception as e:
        return {"safe": False, "error": str(e)}


def zip_scanner_app():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("🗂 Neon ZIP File Scanner")

    st.markdown('<span class="red-label">Upload ZIP File</span>', unsafe_allow_html=True)
    zip_file = st.file_uploader("", type=["zip"])

    if zip_file:
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{zip_file.name}"

        with open(file_path, "wb") as f:
            f.write(zip_file.getbuffer())

        st.info(f"🔍 Scanning {zip_file.name}...")

        # Progress bar animation
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)

        result = scan_zip(file_path)

        if "error" in result:
            st.error(f"❌ Error scanning ZIP: {result['error']}")
            return

        if not result["safe"]:
            st.markdown(f'<div class="threat-box">{result["threat"]}</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="flags-box"><b>🚩 Suspicious Files:</b><br>' +
                "<br>".join(result["flags"]) +
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="solution-box"><b>🛡 How to Protect:</b><br>' +
                "<br>".join(result["solution"]) +
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.success("✔ ZIP is safe ✅")

    st.markdown("</div>", unsafe_allow_html=True)


# Run the app
zip_scanner_app()
