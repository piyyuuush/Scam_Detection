import streamlit as st
import zipfile
import os

def scan_zip(file_path: str):
    try:
        with zipfile.ZipFile(file_path, "r") as z:
            files = z.namelist()

        suspicious = [f for f in files if f.endswith((".exe", ".bat", ".cmd", ".scr"))]

        if suspicious:
            return {
                "safe": False,
                "threat": "Suspicious Files Found",
                "flags": suspicious,
                "solution": [
                    "Do NOT extract unknown ZIP files",
                    "Never run EXE/BAT files from email ZIPs",
                    "Scan ZIP with antivirus"
                ]
            }

        return {
            "safe": True,
            "threat": "No Threat Detected",
            "flags": [],
            "solution": ["ZIP looks safe"]
        }

    except Exception as e:
        return {"safe": False, "error": str(e)}


def zip_scanner_app():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("🗂 ZIP File Scanner")

    zip_file = st.file_uploader("Upload ZIP File", type=["zip"])

    if zip_file:
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{zip_file.name}"

        with open(file_path, "wb") as f:
            f.write(zip_file.getbuffer())

        st.info(f"Scanning {zip_file.name}...")

        result = scan_zip(file_path)

        if "error" in result:
            st.error(f"Error scanning ZIP: {result['error']}")
            return

        if not result["safe"]:
            st.markdown(
                f'<div class="threat-box">{result["threat"]}</div>',
                unsafe_allow_html=True,
            )
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
            st.success("✔ ZIP is safe")

    st.markdown("</div>", unsafe_allow_html=True)