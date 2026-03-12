import streamlit as st
import joblib
import time
import random

# =================== FULL BLACK CYBERPUNK THEME CSS ===================
st.markdown("""
<style>

/* ---------- GLOBAL PAGE BACKGROUND ---------- */
html, body, [class*="stApp"] {
    background-color: black !important;
}

/* ---------- TITLE COLOR ---------- */
h1 {
    color: black !important;
}

/* ---------- CARD BOXES ---------- */
.card {
    background: black !important;
    border: 2px solid #00ffcc55;
    border-radius: 25px;
    padding: 25px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px #00ffcc88;
    animation: fadeIn 1s ease forwards;
}

/* ---------- TABS ---------- */
.stTabs [data-baseweb="tab-list"] {
    background-color: black !important;
    border-bottom: 2px solid #00ffcc55;
}

.stTabs [data-baseweb="tab"] {
    background-color: black !important;
    color: #00ffcc !important;
    border-radius: 10px;
    padding: 10px;
}

.stTabs [aria-selected="true"] {
    background-color: #001a1a !important;
    border-bottom: 3px solid #00ffcc !important;
}

/* ---------- TEXT AREA ---------- */
textarea {
    background-color: black;
    color: black;
    border: 2px solid #00ffcc55 !important;
    border-radius: 12px !important;
}

/* ---------- BUTTONS ---------- */
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

/* ---------- MATRIX LINES ---------- */
.matrix-line {
    font-family: monospace;
    color: #00ff88;
    line-height:1.3;
    font-size:14px;
}

/* ---------- LIST COLORS ---------- */
.red-flags li { color:#ff4d6d; font-weight:bold; margin-bottom:10px; }
.protection li { color:#00ffcc; font-weight:bold; margin-bottom:10px; }
.example-email li { color:#ffcc00; font-weight:bold; margin-bottom:10px; }

/* ---------- THREAT ALERT ---------- */
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

        scan_container.markdown(
            f'<div class="matrix-line">{fake_chars}</div>',
            unsafe_allow_html=True
        )
        time.sleep(0.03)

        scan_container.markdown(
            f'<div class="matrix-line">{line}</div>',
            unsafe_allow_html=True
        )
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
        st.markdown(
            f'<div class="threat-alert" style="color:#00ff88; text-shadow:0 0 5px #00ff88,0 0 15px #00ffcc;">SAFE EMAIL — Confidence: {confidence:.1f}%</div>',
            unsafe_allow_html=True
        )



# =================== APP FUNCTION ===================
def app():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.title("✉️ Cyberpunk Phishing Email Checker")

    # Tabs
    tabs = st.tabs(["🔎 Detection", "⚠ Red Flags", "🛡 Protection Tips", "💀 Example Emails"])

    # User Input
    email_text = st.text_area("Paste Email Content Here", height=220)

    # Detect Button
    if st.button("🔎 Detect Phishing"):
        if not email_text.strip():
            st.warning("⚠ Please enter an email!")
        else:
            with tabs[0]:
                st.markdown('<div class="card"><h4>🖥 Analyzing email line by line...</h4></div>',
                            unsafe_allow_html=True)
                matrix_scan(email_text)

            model, vectorizer = load_model()

            if model:
                X = vectorizer.transform([email_text])
                pred = model.predict(X)[0]
                prob = model.predict_proba(X)[0]

                # Result
                with tabs[0]:
                    if pred == 1:
                        st.markdown('<div class="threat-box">💀 PHISHING DETECTED</div>',
                                    unsafe_allow_html=True)
                        show_threat_alert(prob[1], phishing=True)
                    else:
                        show_threat_alert(prob[0], phishing=False)

                # Red Flags
                with tabs[1]:
                    st.markdown(
                        '<div class="card"><h4>⚠ Red Flags:</h4>'
                        '<ul class="red-flags">'
                        '<li>Sender domain mismatch</li>'
                        '<li>Suspicious or shortened links</li>'
                        '<li>Urgent tone</li>'
                        '<li>Generic greeting</li>'
                        '<li>Grammar mistakes</li>'
                        '<li>Unexpected attachments</li>'
                        '<li>Requests for passwords/OTP</li>'
                        '</ul></div>',
                        unsafe_allow_html=True
                    )

                # Protection Tips
                with tabs[2]:
                    st.markdown(
                        '<div class="card"><h4>🛡 Protection Tips:</h4>'
                        '<ul class="protection">'
                        '<li>Verify the sender address</li>'
                        '<li>Hover over links before clicking</li>'
                        '<li>Enable Two-Factor Authentication</li>'
                        '<li>Never share OTP or passwords</li>'
                        '</ul></div>',
                        unsafe_allow_html=True
                    )

                # Example Fake Email
                with tabs[3]:
                    st.markdown(
                        '<div class="card"><h4>💀 Fake Email Example:</h4>'
                        '<ul class="example-email">'
                        '<li>From: support@fakebank.com</li>'
                        '<li>Subject: Urgent! Verify Account</li>'
                        '<li>Message: Click the link below</li>'
                        '</ul></div>',
                        unsafe_allow_html=True
                    )

    st.markdown("</div>", unsafe_allow_html=True)



# =================== RUN APP ===================
if __name__ == "__main__":
    app()