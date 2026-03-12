from __future__ import annotations
from pathlib import Path
import streamlit as st
import pandas as pd

# ------------------ Import Page Modules ------------------
from cyberthreatdetect.ui.phishing_checker import app as phishing_app
from cyberthreatdetect.ui.apk_scanner import apk_scanner_app
from cyberthreatdetect.ui.zip_scanner import zip_scanner_app
from cyberthreatdetect.ui.spam_checker import spam_checker_app
from cyberthreatdetect.ui.about import about_app

# ------------------ Page Config ------------------
st.set_page_config(page_title="CyberThreatDetect", layout="wide", initial_sidebar_state="expanded")

# ------------------ Hide Streamlit Header/Footer ------------------
st.markdown("""
<style>
header {visibility: hidden;}
footer {visibility: hidden;}
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ------------------ Session State ------------------
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"

# ------------------ Cyberpunk CSS ------------------
st.markdown("""
<style>
html, body, .stApp {
    background: url('https://greymatter.com/wp-content/uploads/2024/06/Cyber-security-news-header.png') no-repeat center center fixed;
    background-size: cover;
    color: white;
}
.stApp::before {
    content:"";
    position:fixed;
    top:0; left:0;
    width:100%; height:100%;
    background: rgba(0,0,0,0.6);
    z-index:-1;
}
[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.25) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid #00ffcc55;
}
.stButton>button {
    background-color: #26c9d6;
    color: white;
    font-size: 17px;
    border-radius: 8px;
    padding: 10px;
    border: none;
    box-shadow: 0 0 10px #00ffcc;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #00ffcc;
    box-shadow: 0 0 20px #00ffcc;
}
.title { font-size:48px; font-weight:bold; text-align:center; color:#070707; margin-top:50px; text-shadow:0 0 12px #00ffcc, 0 0 25px #ff4d6d; }
.subtitle { font-size:24px; text-align:center; color:#ff4d6d; margin-bottom:40px; }
.animated-box { width:80%; margin:auto; padding:30px; background: rgba(0,0,0,0.6); border:2px solid #00ffcc; border-radius:20px; text-align:center; font-size:18px; font-weight:bold; animation: pulse 2s infinite alternate; }
.tip-box { margin: 15px auto; padding: 20px; width: 70%; background: rgba(0,0,0,0.7); border: 2px solid #00ffcc; border-radius: 15px; font-size: 18px; font-weight: bold; display: flex; gap: 15px; }
.neon-title { color: #00ffcc; font-size: 2.2em; text-align:center; text-shadow: 0 0 10px #00ffcc; }
</style>
""", unsafe_allow_html=True)

# ------------------ Top Navbar ------------------
def top_navbar():
    pages = ["🏠 Home","✉️ Phishing","📱 APK Scan","🗂 ZIP Scan","🛑 Spam Check","ℹ️ About"]
    cols = st.columns(len(pages))
    for i, p in enumerate(pages):
        if cols[i].button(p):
            st.session_state["page"] = p
    return st.session_state["page"]

# ------------------ Main Function ------------------
def main():
    # Navbar
    page = top_navbar()

    # Sidebar selectbox
    page = st.sidebar.selectbox(
        "Select Page",
        ["🏠 Home","✉️ Phishing","📱 APK Scan","🗂 ZIP Scan","🛑 Spam Check","ℹ️ About"],
        index=["🏠 Home","✉️ Phishing","📱 APK Scan","🗂 ZIP Scan","🛑 Spam Check","ℹ️ About"].index(st.session_state["page"])
    )
    st.session_state["page"] = page

    # ------------------ Page Routes ------------------
    if page == "🏠 Home":
        st.markdown('<div class="title">🛡️ Welcome to CyberThreatDetect</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">AI-Powered Cybersecurity Platform</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="animated-box">
            Detect Phishing, Spam Messages, APK Malware, and ZIP Viruses
            using real-time AI-powered scanning.
        </div>
        """, unsafe_allow_html=True)

    elif page == "✉️ Phishing":
        phishing_app()
    elif page == "📱 APK Scan":
        apk_scanner_app()
    elif page == "🗂 ZIP Scan":
        zip_scanner_app()
    elif page == "🛑 Spam Check":
        spam_checker_app()
    elif page == "ℹ️ About":
        about_app()

if __name__ == "__main__":
    main()