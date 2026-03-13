import streamlit as st
import joblib
import time
import random
import pandas as pd

# =================== CYBERPUNK THEME CSS ===================
st.markdown("""
<style>
html, body, [class*="stApp"] {
    background-color: black !important;
    color: #00ffcc !important;
    font-family: 'Courier New', monospace;
}

/* Title glow */
h1 {
    color: #00ffcc !important;
    text-shadow: 0 0 10px #00ffcc, 0 0 20px #ff4d6d;
    animation: glowPulse 2s infinite alternate;
}

/* Card boxes */
.card {
    background: #000000 !important;
    border: 2px solid #00ffcc55;
    border-radius: 25px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px #00ffcc88;
    animation: fadeIn 1s ease forwards;
}

/* Text area */
textarea {
    background-color: rgba(0,0,0,0.6);
    color: #00ffcc !important;
    border: 2px solid #00ffcc55 !important;
    border-radius: 12px !important;
    font-family: monospace;
}

/* Buttons */
.stButton>button {
    background: linear-gradient(90deg, #00cc88, #00ffcc);
    color: black;
    font-weight: bold;
    font-size: 20px;
    border-radius: 15px;
    border:none;
    padding: 15px;
    margin-top: 15px;
    box-shadow: 0 0 25px #00ffcc;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background: linear-gradient(90deg, #00ffcc, #ff4d6d);
    box-shadow: 0 0 40px #00ffcc, 0 0 50px #ff4d6d;
    transform: scale(1.05);
}

/* Matrix lines */
.matrix-line {
    font-family: monospace;
    color: #00ff88;
    line-height:1.3;
    font-size:14px;
}

/* Threat alert */
.threat-alert {
    font-size:22px;
    font-weight:bold;
    color:#ff1a1a;
    text-align:center;
    text-shadow:0 0 5px #ff4d6d,0 0 15px #ff0000;
    animation:blink 1s infinite alternate;
}

@keyframes fadeIn {0%{opacity:0;}100%{opacity:1;}}
@keyframes blink {0%{opacity:1;}100%{opacity:0.3;}}
@keyframes glowPulse {from {text-shadow:0 0 5px #00ffcc;} to {text-shadow:0 0 20px #ff4d6d;}}
</style>
""", unsafe_allow_html=True)

# =================== Load Model ===================
def load_model():
    try:
        model = joblib.load("artifacts/phishing_model.pkl")
        vectorizer = joblib.load("artifacts/vectorizer.pkl")
        return model, vectorizer
    except Exception as e:
        st.error(f"❌ Model Load Failed: {e}")
        return None, None

# =================== Matrix Scan Animation ===================
def matrix_scan(email_text):
    lines = email_text.strip().split('\n')
    scan_container = st.empty()

    for line in lines:
        if not line.strip():
            continue
        fake_chars = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789@#$%&*')
                             for _ in range(len(line)))
        scan_container.markdown(f'<div class="matrix-line">{fake_chars}</div>', unsafe_allow_html=True)
        time.sleep(0.03)
        scan_container.markdown(f'<div class="matrix-line">{line}</div>', unsafe_allow_html=True)
        time.sleep(0.03)

# =================== Threat Alert ===================
def show_threat_alert(prob, phishing=True):
    confidence = prob * 100
    if phishing:
        st.markdown(
            f'<div class="threat-alert">⚠ PHISHING ALERT — Confidence: {confidence:.1f}% ⚠</div>',
            unsafe_allow_html=True
        )
    else:
        st.success(f"✔ SAFE EMAIL — Confidence: {confidence:.1f}%")

# =================== APP FUNCTION ===================
def app():
    st.title("✉️ Cyberpunk Phishing Email Checker")

    tabs = st.tabs(["🔎 Detection", "⚠ Red Flags", "🛡 Protection Tips", "💀 Example Emails"])

    email_text = st.text_area("Paste Email Content Here", height=220)

    if st.button("🔎 Detect Phishing"):
        if not email_text.strip():
            st.warning("⚠ Please enter an email!")
        else:
            with tabs[0]:
                st.markdown('<div class="card"><h4>🖥 Analyzing email line by line...</h4></div>', unsafe_allow_html=True)
                matrix_scan(email_text)

            model, vectorizer = load_model()
            if model:
                X = vectorizer.transform([email_text])
                pred = model.predict(X)[0]
                prob = model.predict_proba(X)[0]

                with tabs[0]:
                    col1, col2 = st.columns([2,1])
                    with col1:
                        if pred == 1:
                            show_threat_alert(prob[1], phishing=True)
                        else:
                            show_threat_alert(prob[0], phishing=False)
                    with col2:
                        st.metric("Confidence", f"{(prob[1] if pred==1 else prob[0])*100:.1f}%")

                    # Animated confidence bar
                    st.write("📊 Confidence Level")
                    progress = st.progress(0)
                    target = int((prob[1] if pred==1 else prob[0])*100)
                    for i in range(target):
                        progress.progress(i+1)
                        time.sleep(0.01)

                    

                with tabs[1]:
                    with st.expander("⚠ Red Flags"):
                        st.markdown(
                            '<ul class="red-flags">'
                            '<li>Sender domain mismatch</li>'
                            '<li>Suspicious or shortened links</li>'
                            '<li>Urgent tone</li>'
                            '<li>Generic greeting</li>'
                            '<li>Grammar mistakes</li>'
                            '<li>Unexpected attachments</li>'
                            '<li>Requests for passwords/OTP</li>'
                            '</ul>', unsafe_allow_html=True
                        )

                with tabs[2]:
                    with st.expander("🛡 Protection Tips"):
                        st.markdown(
                            '<ul class="protection">'
                            '<li>Verify the sender address</li>'
                            '<li>Hover over links before clicking</li>'
                            '<li>Enable Two-Factor Authentication</li>'
                            '<li>Never share OTP or passwords</li>'
                            '</ul>', unsafe_allow_html=True
                        )

                with tabs[3]:
                    with st.expander("💀 Example Fake Email"):
                        st.markdown(
                            '<ul class="example-email">'
                            '<li>From: support@fakebank.com</li>'
                            '<li>Subject: Urgent! Verify Account</li>'
                            '<li>Message: Click the link below</li>'
                            '</ul>', unsafe_allow_html=True
                        )

# =================== RUN APP ===================
if __name__ == "__main__":
    app()
