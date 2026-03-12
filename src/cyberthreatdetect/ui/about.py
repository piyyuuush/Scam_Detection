import streamlit as st

def about_app():
    st.markdown("""
    <style>
    body { background-color: #0d0d0d; color: #ffffff; font-family: 'Courier New', monospace; }

    .card { background: rgba(0,0,0,0.6); border: 2px solid #00ffea; border-radius: 20px; padding: 30px; margin-bottom: 30px; box-shadow: 0 0 20px #00ffea; transition: all 0.3s ease-in-out; }

    .section-title { font-size: 32px; color: #00ffea; text-shadow: 0 0 5px #00ffea, 0 0 10px #00ffea, 0 0 20px #00ffea; animation: flicker 1.5s infinite alternate; margin-bottom: 20px; }
    .sub-title { font-size: 22px; font-weight: bold; color: #ff4d6d; margin-top: 20px; margin-bottom: 10px; text-shadow: 0 0 5px #ff4d6d; }

    @keyframes flicker { 0%,19%,21%,23%,25%,54%,56%,100% { opacity:1; } 20%,22%,24%,55% { opacity:0.4; } }

    .marquee { width: 100%; overflow: hidden; white-space: nowrap; box-sizing: border-box; border-bottom: 1px solid #00ffea; margin-bottom: 30px; }
    .marquee span { display: inline-block; padding-left: 100%; animation: marquee 15s linear infinite; color: #00ffea; font-weight: bold; }
    @keyframes marquee { 0% { transform: translate(0,0); } 100% { transform: translate(-100%,0); } }

    /* Animated cards with delay */
    .feature-card, .step-card, .dev-card { 
        background: rgba(0,0,0,0.4); 
        border-left: 4px solid #00ffea; 
        padding: 15px; margin-bottom: 15px; border-radius: 10px; 
        opacity: 0; transform: translateY(20px); 
        animation: fadeInUp 0.8s forwards; 
    }
    .step-card { border-left: 4px solid #ff4d6d; }
    .dev-card { border-left: 4px solid #00ffea; }

    .feature-card:hover, .step-card:hover, .dev-card:hover { 
        transform: translateY(-5px); 
        box-shadow: 0 0 20px #00ffea; 
    }

    @keyframes fadeInUp { 0% { opacity: 0; transform: translateY(20px); } 100% { opacity: 1; transform: translateY(0); } }

    /* Icon pulse */
    .icon { display:inline-block; animation: pulse 1.5s infinite alternate; }
    @keyframes pulse { 0% { text-shadow:0 0 5px #00ffea; } 100% { text-shadow:0 0 20px #00ffea; } }

    a { color:#00ffea; text-decoration:none; }
    a:hover { text-decoration:underline; }
    </style>
    """, unsafe_allow_html=True)

    # Marquee
    st.markdown('<div class="marquee"><span>CyberThreatDetect — Advanced AI-Powered Cybersecurity Platform</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.markdown('<div class="section-title">ℹ️ About CyberThreatDetect</div>', unsafe_allow_html=True)
    st.markdown("""
    CyberThreatDetect is an AI-powered cybersecurity platform that protects against phishing, malware, APK threats, and spam messages.  
    Its mission is to empower users and organizations with real-time threat detection, analysis, and actionable recommendations.
    """)

    st.markdown('<div class="sub-title">🔍 Key Features</div>', unsafe_allow_html=True)
    features = [
        "✉️ <span class='icon'>📧</span> **Phishing Email Detection** – Analyzes emails for phishing attacks using NLP and sender patterns.",
        "🗂 <span class='icon'>💻</span> **ZIP & APK Malware Scanning** – Detects malicious scripts and APKs before they harm your system.",
        "🛑 <span class='icon'>⚠️</span> **Spam Message Filtering** – Identifies potential spam across SMS and messaging apps.",
        "📊 <span class='icon'>📈</span> **Machine Learning Metrics & Analysis** – Real-time precision, recall, and F1-score for detection models.",
        "🔐 <span class='icon'>🔎</span> **Permission & Signature Analysis** – Checks file permissions and digital signatures to detect anomalies.",
        "📑 <span class='icon'>📝</span> **Real-Time Risk Reports** – Generates actionable reports to reduce cybersecurity risk."
    ]
    # Add animation delays
    for i, feature in enumerate(features):
        st.markdown(f'<div class="feature-card" style="animation-delay:{i*0.3}s">{feature}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sub-title">⚙️ How It Works</div>', unsafe_allow_html=True)
    steps = [
        "1️⃣ <span class='icon'>🗂️</span> **Data Collection** – Gathers emails, ZIP files, APKs, and network logs.",
        "2️⃣ <span class='icon'>🧹</span> **Preprocessing & Feature Extraction** – Cleans and structures data for ML models.",
        "3️⃣ <span class='icon'>🤖</span> **Threat Prediction** – Uses Random Forest, XGBoost, and Neural Networks for detection.",
        "4️⃣ <span class='icon'>📊</span> **Analysis & Reporting** – Creates detailed reports and visual dashboards.",
        "5️⃣ <span class='icon'>📡</span> **User Alerts** – Sends notifications for high-risk threats or anomalies."
    ]
    for i, step in enumerate(steps):
        st.markdown(f'<div class="step-card" style="animation-delay:{i*0.3 + 1.5}s">{step}</div>', unsafe_allow_html=True)

    st.markdown('<div class="sub-title">👨‍💻 Developer</div>', unsafe_allow_html=True)
    dev_info = [
        "**Piyush Kumar Mandal** – B.Tech Computer Engineering (LPU)",
        "**Skills:** Full Stack Development (React, Node.js, Laravel), Cybersecurity, Machine Learning & AI, Python, Java, JavaScript",
        "Passionate about building **secure, intelligent, and user-friendly applications** that protect digital environments.",
        "📧 <a href='mailto:your-email@example.com'>your-email@example.com</a>",
        "GitHub: <a href='https://github.com/your-profile' target='_blank'>github.com/your-profile</a>",
        "LinkedIn: <a href='https://linkedin.com/in/your-profile' target='_blank'>linkedin.com/in/your-profile</a>"
    ]
    for i, info in enumerate(dev_info):
        st.markdown(f'<div class="dev-card" style="animation-delay:{i*0.3 + 3.5}s">{info}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)