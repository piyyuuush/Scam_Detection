from __future__ import annotations
import streamlit as st

# ── MUST be first Streamlit call ─────────────────────────────────────────────
st.set_page_config(page_title="CyberThreatDetect", layout="wide", page_icon="🛡️")

# ── Page imports AFTER set_page_config ───────────────────────────────────────
from cyberthreatdetect.ui.phishing_checker import app as phishing_app
from cyberthreatdetect.ui.url_scanner import url_scanner_app
from cyberthreatdetect.ui.zip_scanner import zip_scanner_app
from cyberthreatdetect.ui.spam_checker import spam_checker_app
from cyberthreatdetect.ui.about import about_app

# ── Session State ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "🏠 Home"
if "dark_mode" not in st.session_state:
    st.session_state["dark_mode"] = True   # default: dark

PAGES = ["🏠 Home", "✉️ Phishing", "📱 URL Scan", "🗂 ZIP Scan", "🛑 Spam Check", "ℹ️ About"]

# ── Theme Variables ───────────────────────────────────────────────────────────
def theme():
    dark = st.session_state["dark_mode"]
    if dark:
        return dict(
            bg            = "#020c14",
            bg2           = "rgba(0,0,0,0.50)",
            bg3           = "rgba(0,20,30,0.85)",
            sidebar_bg    = "rgba(2,12,20,0.97)",
            border        = "#00ffcc22",
            border2       = "#00ffcc44",
            accent        = "#00ffcc",
            accent2       = "#ff4d6d",
            text          = "#e0ffff",
            text_muted    = "#94a3b8",
            tip_bg        = "rgba(0,0,0,0.45)",
            tip_text      = "#c0ffe8",
            card_bg       = "rgba(0,0,0,0.50)",
            info_bg       = "rgba(0,20,30,0.6)",
            grid_color    = "rgba(0,255,204,0.025)",
            input_bg      = "rgba(0,20,30,0.85)",
            input_color   = "#e0ffff",
            btn_bg        = "rgba(0,255,204,0.08),rgba(0,200,160,0.12)",
            btn_bg_hover  = "rgba(0,255,204,0.20),rgba(0,200,160,0.25)",
            btn_color     = "#00ffcc",
            btn_border    = "#00ffcc44",
            prog_bar      = "linear-gradient(90deg,#00ffcc,#0ea5e9)",
            step_bg       = "rgba(0,0,0,0.35)",
            footer_border = "#00ffcc22",
            footer_color  = "#00ffcc33",
            expander_bg   = "rgba(0,255,204,0.04)",
        )
    else:
        return dict(
            bg            = "#f0f4f8",
            bg2           = "rgba(255,255,255,0.92)",
            bg3           = "rgba(255,255,255,0.95)",
            sidebar_bg    = "rgba(240,244,248,0.98)",
            border        = "#2563eb22",
            border2       = "#2563eb44",
            accent        = "#2563eb",
            accent2       = "#dc2626",
            text          = "#1e293b",
            text_muted    = "#64748b",
            tip_bg        = "rgba(255,255,255,0.85)",
            tip_text      = "#1e293b",
            card_bg       = "rgba(255,255,255,0.90)",
            info_bg       = "rgba(239,246,255,0.9)",
            grid_color    = "rgba(37,99,235,0.04)",
            input_bg      = "rgba(255,255,255,0.95)",
            input_color   = "#1e293b",
            btn_bg        = "rgba(37,99,235,0.08),rgba(37,99,235,0.12)",
            btn_bg_hover  = "rgba(37,99,235,0.18),rgba(37,99,235,0.22)",
            btn_color     = "#2563eb",
            btn_border    = "#2563eb44",
            prog_bar      = "linear-gradient(90deg,#2563eb,#0ea5e9)",
            step_bg       = "rgba(239,246,255,0.8)",
            footer_border = "#2563eb22",
            footer_color  = "#2563eb55",
            expander_bg   = "rgba(37,99,235,0.04)",
        )

# ── Global CSS ────────────────────────────────────────────────────────────────
def inject_css():
    T = theme()
    dark = st.session_state["dark_mode"]
    glow = f"0 0 30px rgba(0,255,204,0.5),0 0 60px rgba(0,255,204,0.2)" if dark else f"none"
    title_color = T["accent"]
    sidebar_border = "#00ffcc22" if dark else "#2563eb22"

    st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Rajdhani:wght@400;500;600;700&display=swap');

html, body, .stApp {{
    background-color: {T["bg"]} !important;
    color: {T["text"]};
    font-family: 'Rajdhani', sans-serif;
    transition: background-color 0.4s ease, color 0.3s ease;
}}
.stApp::before {{
    content:"";position:fixed;top:0;left:0;width:100%;height:100%;
    background-image:
        linear-gradient({T["grid_color"]} 1px,transparent 1px),
        linear-gradient(90deg,{T["grid_color"]} 1px,transparent 1px);
    background-size:44px 44px;z-index:-1;
}}
header[data-testid="stHeader"],footer,#MainMenu{{visibility:hidden;}}
.block-container{{padding:0.5rem 2rem 3rem;max-width:1400px;}}

[data-testid="stSidebar"]{{
    background:{T["sidebar_bg"]}!important;
    backdrop-filter:blur(20px);
    border-right:1px solid {sidebar_border};
    transition:background 0.4s ease;
}}

.stButton>button{{
    background:linear-gradient(135deg,{T["btn_bg"]})!important;
    color:{T["btn_color"]}!important;
    font-family:'Rajdhani',sans-serif!important;
    font-size:14px!important;font-weight:700!important;
    letter-spacing:0.04em!important;
    border-radius:8px!important;padding:7px 14px!important;
    border:1px solid {T["btn_border"]}!important;
    transition:all 0.2s ease!important;
}}
.stButton>button:hover{{
    background:linear-gradient(135deg,{T["btn_bg_hover"]})!important;
    border-color:{T["accent"]}!important;
    transform:translateY(-1px)!important;
    box-shadow:0 4px 16px {T["accent"]}44!important;
}}

/* Dark/Light toggle button — special pill style */
div[data-testid="column"]:has(button[kind="secondary"]) .stButton>button,
.theme-toggle .stButton>button {{
    border-radius:50px!important;
    padding:6px 18px!important;
    font-size:13px!important;
}}

.stTextInput>div>div>input,
.stTextArea>div>div>textarea{{
    background:{T["input_bg"]}!important;
    border:1.5px solid {T["border2"]}!important;
    border-radius:10px!important;
    color:{T["input_color"]}!important;
    font-family:'Rajdhani',sans-serif!important;
    font-size:15px!important;
    transition:all 0.3s ease;
}}
.stTextInput>div>div>input:focus,
.stTextArea>div>div>textarea:focus{{
    border-color:{T["accent"]}88!important;
    box-shadow:0 0 12px {T["accent"]}22!important;
}}
[data-testid="stFileUploadDropzone"]{{
    background:{T["input_bg"]}!important;
    border:2px dashed {T["border2"]}!important;
    border-radius:12px!important;
}}
.stSelectbox>div>div{{
    background:{T["input_bg"]}!important;
    border:1.5px solid {T["border2"]}!important;
    color:{T["input_color"]}!important;
    border-radius:10px!important;
}}
.stSpinner>div{{border-top-color:{T["accent"]}!important;}}
.stProgress>div>div{{background:{T["prog_bar"]}!important;}}
.streamlit-expanderHeader{{
    background:{T["expander_bg"]}!important;
    border:1px solid {T["border"]}!important;
    border-radius:10px!important;
    color:{T["accent"]}!important;
}}

/* Label colours */
label, .stTextArea label, .stTextInput label, .stSelectbox label {{
    color:{T["text_muted"]}!important;
}}
/* Metric */
[data-testid="stMetricValue"]{{color:{T["accent"]}!important;}}
[data-testid="stMetricLabel"]{{color:{T["text_muted"]}!important;}}
</style>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
def render_sidebar():
    T = theme()
    dark = st.session_state["dark_mode"]
    with st.sidebar:
        st.markdown(f"""
        <div style="text-align:center;padding:1.2rem 0 0.5rem">
            <div style="font-size:2.8rem;filter:drop-shadow(0 0 12px {T['accent']}88)">🛡️</div>
            <div style="font-family:'Orbitron',monospace;color:{T['accent']};font-size:0.78rem;
                        font-weight:700;margin-top:0.5rem;letter-spacing:0.12em;
                        text-shadow:0 0 10px {T['accent']}88">
                CYBER<br>THREAT<br>DETECT
            </div>
        </div>
        <hr style="border:none;border-top:1px solid {T['border']};margin:1rem 0">
        """, unsafe_allow_html=True)

        for p in PAGES:
            if st.button(p, key=f"sb_{p}", use_container_width=True):
                st.session_state["page"] = p
                st.rerun()

        st.markdown(f"""
        <hr style="border:none;border-top:1px solid {T['border']};margin:1rem 0">
        """, unsafe_allow_html=True)

        # ── Theme toggle in sidebar ──
        toggle_label = "☀️ Light Mode" if dark else "🌙 Dark Mode"
        if st.button(toggle_label, key="sb_theme_toggle", use_container_width=True):
            st.session_state["dark_mode"] = not dark
            st.rerun()

        st.markdown(f"""
        <div style="color:{T['text_muted']};font-size:0.72rem;text-align:center;margin-top:0.5rem">
            🛡️ AI Security System · v1.0
        </div>
        """, unsafe_allow_html=True)


# ── Top Navbar ────────────────────────────────────────────────────────────────
def render_navbar():
    T = theme()
    dark = st.session_state["dark_mode"]
    toggle_label = "☀️" if dark else "🌙"
    toggle_title = "Switch to Light Mode" if dark else "Switch to Dark Mode"

    # Logo + nav buttons + toggle in one row
    nav_cols = st.columns([1.2] + [1]*len(PAGES) + [0.7])

    with nav_cols[0]:
        st.markdown(f"""
        <div style="display:flex;align-items:center;height:38px">
            <span style="font-family:'Orbitron',monospace;color:{T['accent']};font-size:0.95rem;
                         font-weight:900;letter-spacing:0.1em;
                         text-shadow:0 0 10px {T['accent']}66">🛡️ CTD</span>
        </div>
        """, unsafe_allow_html=True)

    for i, p in enumerate(PAGES):
        with nav_cols[i + 1]:
            if st.button(p, key=f"nav_{p}", use_container_width=True):
                st.session_state["page"] = p
                st.rerun()

    # Toggle pill button at far right
    with nav_cols[-1]:
        if st.button(f"{toggle_label} {'Dark' if not dark else 'Light'}", key="nav_theme_toggle", use_container_width=True):
            st.session_state["dark_mode"] = not dark
            st.rerun()

    st.markdown(f'<hr style="border:none;border-top:1px solid {T["border"]};margin:0 0 1.2rem">', unsafe_allow_html=True)


# ── Home Page ─────────────────────────────────────────────────────────────────
def home_page():
    T = theme()
    dark = st.session_state["dark_mode"]
    glow = f"0 0 30px {T['accent']}88,0 0 60px {T['accent']}33" if dark else "none"

    st.markdown(f"""
    <div style="text-align:center;padding:2rem 0 0.5rem">
        <h1 style="font-family:'Orbitron',monospace;font-size:2.6rem;font-weight:900;
                   color:{T['accent']};text-shadow:{glow};
                   letter-spacing:0.05em;margin:0">
            🛡️ CyberThreatDetect
        </h1>
        <p style="color:{T['accent2']};font-size:1.15rem;font-weight:600;letter-spacing:0.1em;margin-top:0.4rem">
            ⚡ AI-Powered Cybersecurity Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="width:82%;margin:1rem auto 2rem;padding:1.4rem 2rem;
                background:{T['bg2']};border:1.5px solid {T['border2']};
                border-radius:16px;text-align:center;color:{T['text']};font-size:1rem;line-height:1.7">
        🔍 Detect <strong>Phishing</strong>, <strong>Spam</strong>, <strong>Malicious URLs</strong>,
        and <strong>ZIP Malware</strong> using real-time AI — all in one platform.
    </div>
    """, unsafe_allow_html=True)

    # Module cards
    c1, c2, c3, c4 = st.columns(4, gap="medium")
    cards = [
        (c1, "✉️", "Phishing Detection",  "Detect deceptive emails trying to steal your credentials.", "✉️ Phishing", "#ff4d6d"),
        (c2, "📱", "URL Scanner",          "Verify if a link is safe or a known phishing threat.",       "📱 URL Scan",  "#f59e0b"),
        (c3, "🗂", "ZIP Malware Scan",     "Scan compressed files for hidden viruses and executables.",  "🗂 ZIP Scan",  "#8b5cf6"),
        (c4, "🛑", "Spam Checker",         "Identify spam, scam offers, and fraudulent messages.",       "🛑 Spam Check","#00b894" if not dark else "#00ffcc"),
    ]
    for col, icon, title, desc, dest, color in cards:
        with col:
            st.markdown(f"""
            <div style="background:{T['card_bg']};border:1.5px solid {color}33;
                        border-top:3px solid {color};border-radius:14px;
                        padding:1.4rem;text-align:center;min-height:160px;
                        box-shadow:0 2px 16px {color}11">
                <div style="font-size:2rem;margin-bottom:0.5rem">{icon}</div>
                <div style="color:{color};font-weight:700;font-size:0.95rem;margin-bottom:0.4rem">{title}</div>
                <div style="color:{T['text_muted']};font-size:0.78rem;line-height:1.6">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Launch →", key=f"card_{dest}", use_container_width=True):
                st.session_state["page"] = dest
                st.rerun()

    # Learn expanders
    st.markdown(f'<h2 style="color:{T["accent"]};font-family:\'Orbitron\',monospace;font-size:1.1rem;text-align:center;margin:2rem 0 1rem;letter-spacing:0.08em">📌 LEARN ABOUT THREATS</h2>', unsafe_allow_html=True)

    expanders = [
        ("✉️ Phishing Attacks", "🔐 What is Phishing?",
         "Hackers pretend to be trusted banks or companies to steal your login details, OTP, or money.",
         ["Fake bank emails claiming your account is suspended","Fake login pages that steal credentials","Malicious email attachments","OTP SMS scams"],
         "✉️ Phishing"),
        ("🛑 Spam Messages", "🛑 What is Spam?",
         "Spam includes fake offers, job scams, lottery fraud, and malicious links to steal your money.",
         ["Fake promotions and too-good-to-be-true offers","Lottery and prize scams","Messages with dangerous links","Fake job offers requesting upfront payments"],
         "🛑 Spam Check"),
        ("📱 URL Threats", "📱 What is a Malicious URL?",
         "A harmful website link designed to steal your credentials or install malware on your device.",
         ["Fake banking login pages","Gift/lottery websites collecting your data","Phishing links in emails and SMS","Drive-by malware downloads"],
         "📱 URL Scan"),
        ("🗂 ZIP Malware", "🗂 What is ZIP Malware?",
         "ZIP Malware hides viruses inside compressed folders that infect your system when extracted.",
         ["Hidden .exe files inside harmless-looking ZIPs","Trojan malware via email attachments","Spyware that auto-installs on extraction","Fake invoice ZIPs containing ransomware"],
         "🗂 ZIP Scan"),
    ]
    for title, heading, desc, steps, dest in expanders:
        with st.expander(title):
            st.markdown(f"""
            <div style="background:{T['info_bg']};border:1.5px solid {T['border2']};
                        border-radius:12px;padding:1.2rem 1.6rem;margin-bottom:0.8rem;color:{T['text']}">
                <strong style="color:{T['accent']};font-size:1rem">{heading}</strong><br><br>{desc}
            </div>
            """, unsafe_allow_html=True)
            for s in steps:
                st.markdown(f'<div style="border-left:4px solid {T["accent"]};padding:8px 14px;background:{T["step_bg"]};border-radius:0 8px 8px 0;margin:5px 0;color:{T["text"]};font-size:0.9rem">▸ {s}</div>', unsafe_allow_html=True)
            if st.button(f"Go to {title.split()[0]} →", key=f"exp_{dest}"):
                st.session_state["page"] = dest
                st.rerun()

    # Cyber tips
    st.markdown(f'<h2 style="color:{T["accent"]};font-family:\'Orbitron\',monospace;font-size:1.1rem;text-align:center;margin:2rem 0 1rem;letter-spacing:0.08em">💡 CYBERSECURITY TIPS</h2>', unsafe_allow_html=True)
    tips = [
        ("fa-lock",          "Use strong, unique passwords for every account."),
        ("fa-envelope",      "Never click on links from unknown senders."),
        ("fa-key",           "Enable Two-Factor Authentication (2FA) everywhere."),
        ("fa-wifi",          "Avoid public Wi-Fi for banking or payments."),
        ("fa-shield-halved", "Keep your antivirus and OS updated regularly."),
        ("fa-database",      "Back up your data to avoid ransomware loss."),
    ]
    for icon, text in tips:
        st.markdown(f"""
        <div style="margin:8px auto;padding:13px 20px;width:78%;
                    background:{T['tip_bg']};border:1px solid {T['border2']};
                    border-left:4px solid {T['accent']};border-radius:0 12px 12px 0;
                    font-size:0.92rem;display:flex;align-items:center;gap:14px;color:{T['tip_text']}">
            <i class="fas {icon}" style="color:{T['accent']};width:18px;text-align:center"></i> {text}
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="text-align:center;padding:2rem 0 0.5rem;border-top:1px solid {T['footer_border']};
                margin-top:2.5rem;color:{T['footer_color']};font-size:0.78rem;letter-spacing:0.1em">
        🛡️ AI SECURITY SYSTEM · CYBERTHREATDETECT
    </div>
    """, unsafe_allow_html=True)


# ── Router ────────────────────────────────────────────────────────────────────
def main():
    inject_css()
    render_sidebar()
    render_navbar()

    page = st.session_state["page"]
    if page == "🏠 Home":
        home_page()
    elif page == "✉️ Phishing":
        phishing_app()
    elif page == "📱 URL Scan":
        url_scanner_app()
    elif page == "🗂 ZIP Scan":
        zip_scanner_app()
    elif page == "🛑 Spam Check":
        spam_checker_app()
    elif page == "ℹ️ About":
        about_app()


if __name__ == "__main__":
    main()