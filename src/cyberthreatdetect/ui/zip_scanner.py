import streamlit as st
import zipfile
import os
import time

# --- Custom CSS ---
st.markdown("""
    <style>
        .card {
            background-color: #f9f9f9;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        .red-label {
            color: red;
            font-weight: bold;
            font-size: 18px;
        }
        .threat-box {
            background-color: #ffcccc;
            color: #a80000;
            padding: 15px;
            border-radius: 8px;
            margin-top: 15px;
            font-weight: bold;
            font-size: 16px;
        }
        .flags-box {
            background-color: #fff3cd;
            color: #856404;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 14px;
        }
        .solution-box {
            background-color: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-top: 10px;
            font-size: 14px;
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
    st.title("🗂 ZIP File Scanner")

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
            time.sleep(0.02)  # adjust speed here
            progress_bar.progress(percent_complete + 1)

        result = scan_zip(file_path)

        if "error" in result:
            st.error(f"❌ Error scanning ZIP: {result['error']}")
            return

        if not result["safe"]:
            st.markdown(f'<div class="threat-box">{result["threat"]}</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="flags-box"><b>Suspicious Files:</b><br>' +
                "<br>".join(result["flags"]) +
                "</div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                '<div class="solution-box"><b>How to Protect:</b><br>' +
                "<br>".join(result["solution"]) +
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            st.success("✔ ZIP is safe ✅")

    st.markdown("</div>", unsafe_allow_html=True)


# Run the app
zip_scanner_app()
