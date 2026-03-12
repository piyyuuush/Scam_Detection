from __future__ import annotations
from pathlib import Path
import pandas as pd
import streamlit as st

# Import page modules
from cyberthreatdetect.ui.phishing_checker import app as phishing_app
from cyberthreatdetect.ui.apk_scanner import apk_scanner_app
from cyberthreatdetect.ui.zip_scanner import zip_scanner_app
from cyberthreatdetect.ui.spam_checker import spam_checker_app
from cyberthreatdetect.ui.about import about_app

st.set_page_config(page_title="CyberThreatDetect", layout="wide")

# Hide Streamlit default header, footer, and menu
st.markdown("""
<style>
/* Hide the top header (Deploy + menu) */
header[data-testid="stHeader"] {visibility: hidden;}

/* Hide the footer ("Made with Streamlit") */
footer {visibility: hidden;}

/* Optional: hide hamburger menu */
#MainMenu {visibility: hidden;}
</style>
""", unsafe_allow_html=True)
# =================== SESSION STATE INITIALIZATION ===================
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"

# =================== GLOBAL CYBERPUNK THEME ===================
st.markdown("""
<style>
html, body, .stApp {
    background: url('https://greymatter.com/wp-content/uploads/2024/06/Cyber-security-news-header.png') no-repeat center center fixed;
    background-size: cover;
    color: white;
}

/* BG dark overlay */
.stApp::before {
    content:"";
    position:fixed;
    top:0; left:0; 
    width:100%; height:100%;
    background: rgba(0,0,0,0.6);
    z-index:-1;
}

/* Transparent Sidebar */
[data-testid="stSidebar"] {
    background: rgba(0,0,0,0.25) !important;
    backdrop-filter: blur(15px);
    border-right: 1px solid #00ffcc55;
}

/* Buttons */
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

/* Headings */
.title {
    font-size:48px;
    font-weight:bold;
    text-align:center;
    color:#070707;
    margin-top:50px;
    text-shadow:0 0 12px #00ffcc, 0 0 25px #ff4d6d;
}
.subtitle {
    font-size:24px;
    text-align:center;
    color:#ff4d6d;
    margin-bottom:40px;
}

/* Animated Box */
.animated-box {
    width:80%;
    margin:auto;
    padding:30px;
    background: rgba(0,0,0,0.6);
    border:2px solid #00ffcc;
    border-radius:20px;
    text-align:center;
    font-size:18px;
    font-weight:bold;
    animation: pulse 2s infinite alternate;
}

/* Tips */
.tip-box {
    margin: 15px auto;
    padding: 20px;
    width: 70%;
    background: rgba(0,0,0,0.7);
    border: 2px solid #00ffcc;
    border-radius: 15px;
    font-size: 18px;
    font-weight: bold;
    display: flex;
    gap: 15px;
}

/* Neon expanders */
#phishing-expander span[data-testid="stExpanderLabel"],
#spam-expander span[data-testid="stExpanderLabel"],
#apk-expander span[data-testid="stExpanderLabel"],
#zip-expander span[data-testid="stExpanderLabel"] {
    font-size: 28px !important;
    font-weight: 900 !important;
    color: #00ffcc !important;
    text-shadow: 0 0 15px #00ffcc;
}

/* Info Box */
.info-box {
    background: rgba(0,0,0,0.5);
    border: 2px solid #00ffcc;
    padding: 20px;
    border-radius: 15px;
    margin-top: 15px;
    box-shadow: 0 0 15px #00ffcc55;
}

/* Timeline */
.timeline-step {
    background: rgba(0,0,0,0.4);
    border-left: 5px solid #00ffcc;
    padding: 12px;
    border-radius: 10px;
    margin-top: 10px;
}

.big-text { font-size: 20px; color:#e0ffff; }
.mid-text { font-size: 19px; color:#d0ffff; }

.neon-title {
    color: #00ffcc;
    font-size: 2.2em;
    text-align:center;
    text-shadow: 0 0 10px #00ffcc;
}
</style>
<link rel="stylesheet"
href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)

# ---------------------- TOP NAVBAR ----------------------
def top_navbar():
    pages = ["🏠 Home","✉️ Phishing","📱 APK Scan","🗂 ZIP Scan","🛑 Spam Check","ℹ️ About"]
    cols = st.columns(len(pages))

    for i, p in enumerate(pages):
        if cols[i].button(p):
            st.session_state["page"] = p

    return st.session_state["page"]

# =================== MAIN ===================
def main():
    st.set_page_config(page_title="CyberThreatDetect", layout="wide")

    # Navbar
    page = top_navbar()

    # Sidebar selectbox
    page = st.sidebar.selectbox(
        "Select Page",
        ["🏠 Home","✉️ Phishing","📱 APK Scan","🗂 ZIP Scan","🛑 Spam Check","ℹ️ About"],
        index=["🏠 Home","✉️ Phishing","📱 APK Scan","🗂 ZIP Scan","🛑 Spam Check","ℹ️ About"].index(st.session_state["page"])
    )
    st.session_state["page"] = page

    # ---------------- HOME PAGE ----------------
    if page == "🏠 Home":
        st.markdown('<div class="title">🛡️ Welcome to CyberThreatDetect</div>', unsafe_allow_html=True)
        st.markdown('<div class="subtitle">AI-Powered Cybersecurity Platform</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="animated-box">
            Detect Phishing, Spam Messages, APK Malware, and ZIP Viruses
            using real-time AI-powered scanning.
        </div>
        """, unsafe_allow_html=True)

        # ---------- Phishing expander ----------
        st.markdown("<div id='phishing-expander'>", unsafe_allow_html=True)
        with st.expander("📌 Learn About Phishing"):
            st.markdown("""
            <div class="info-box big-text">
                <b>🔐 What is Phishing?</b><br><br>
                Phishing is a cyber attack where hackers pretend to be trusted banks,
                companies, or government portals to steal your login details, OTP, or money.
            </div>

            <div class="timeline-step mid-text">⚠ Fake bank emails.</div>
            <div class="timeline-step mid-text">🔗 Fake login pages.</div>
            <div class="timeline-step mid-text">📎 Malware attachments.</div>
            <div class="timeline-step mid-text">📱 OTP SMS scams.</div>
            """, unsafe_allow_html=True)

            if st.button("🚀 Start Phishing Detection"):
                st.session_state["page"] = "✉️ Phishing"

        # ---------- Spam expander ----------
        st.markdown("<div id='spam-expander'>", unsafe_allow_html=True)
        with st.expander("📌 Learn About Spam Messages"):
            st.markdown("""
            <div class="info-box big-text">
                <b>🛑 What is Spam?</b><br><br>
                Spam messages include fake offers, job scams, lottery fraud,
                and malicious links meant to steal your money or data.
            </div>

            <div class="timeline-step mid-text">📢 Fake promotions.</div>
            <div class="timeline-step mid-text">💰 Lottery scams.</div>
            <div class="timeline-step mid-text">⚠ Dangerous URLs.</div>
            <div class="timeline-step mid-text">👔 Fake job offers.</div>
            """, unsafe_allow_html=True)

            if st.button("📤 Start Spam Detection"):
                st.session_state["page"] = "🛑 Spam Check"

        # ---------- APK expander ----------
        st.markdown("<div id='apk-expander'>", unsafe_allow_html=True)
        with st.expander("📌 Learn About APK Malware"):
            st.markdown("""
            <div class="info-box big-text">
                <b>📱 What is APK Malware?</b><br><br>
                APK Malware is harmful Android software that can track your activity,
                steal passwords, access banking apps, or fully control your device.
            </div>

            <div class="timeline-step mid-text">⚠ Fake banking/UPI apps.</div>
            <div class="timeline-step mid-text">📦 Apps from Telegram or MediaFire.</div>
            <div class="timeline-step mid-text">🕵 Hidden spyware or keyloggers.</div>
            <div class="timeline-step mid-text">💀 Ransomware APK files.</div>
            """, unsafe_allow_html=True)

            if st.button("📱 Start APK Scan"):
                st.session_state["page"] = "📱 APK Scan"

        # ---------- ZIP expander ----------
        st.markdown("<div id='zip-expander'>", unsafe_allow_html=True)
        with st.expander("📌 Learn About ZIP Malware"):
            st.markdown("""
            <div class="info-box big-text">
                <b>🗂 What is ZIP Malware?</b><br><br>
                ZIP Malware hides viruses inside compressed folders.
                These files infect your system when you extract them.
            </div>

            <div class="timeline-step mid-text">📦 Hidden .exe inside ZIP.</div>
            <div class="timeline-step mid-text">💣 Trojan malware in attachments.</div>
            <div class="timeline-step mid-text">🕵 Spyware auto-install.</div>
            <div class="timeline-step mid-text">⚠ Fake invoice ZIP emails.</div>
            """, unsafe_allow_html=True)

            if st.button("🗂 Start ZIP Scan"):
                st.session_state["page"] = "🗂 ZIP Scan"

        # ---------- Cyber Tips ----------
        st.markdown('<h2 class="neon-title" style="margin-top:40px;">💡 Cybersecurity Tips</h2>', unsafe_allow_html=True)
        tips = [
            ("fa-lock", "Use strong unique passwords."),
            ("fa-envelope", "Avoid clicking unknown links."),
            ("fa-key", "Enable 2FA authentication."),
            ("fa-wifi", "Avoid public Wi-Fi for payments."),
            ("fa-shield-halved", "Keep antivirus updated."),
            ("fa-database", "Backup data often."),
        ]
        for icon, text in tips:
            st.markdown(f"""
            <div class="tip-box">
                <i class="fas {icon}"></i> {text}
            </div>
            """, unsafe_allow_html=True)

    # ---------------- PAGE ROUTES ----------------
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