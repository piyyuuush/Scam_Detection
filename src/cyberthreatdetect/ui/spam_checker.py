# app_streamlit_cyberpunk_ui_v7.py
import streamlit as st
import joblib
import pandas as pd
import re
from pathlib import Path

# ----------------- Load Pipeline -----------------
def load_pipeline(path: str):
    p = Path(path)
    if not p.exists():
        st.error(f"❌ Pipeline file not found at {path}")
        return None
    return joblib.load(p)

# ----------------- Highlight Spam Keywords -----------------
SPAM_KEYWORDS = [
    "win", "free", "cash", "gift", "prize", "urgent", "click", "verify",
    "reward", "congratulations", "loan", "account", "limited", "offer"
]

def highlight_keywords(text):
    highlighted = text
    for kw in SPAM_KEYWORDS:
        highlighted = re.sub(
            f"(?i)\\b{kw}\\b",
            f"<span class='neon-keyword'>{kw}</span>",
            highlighted
        )
    return highlighted

# ----------------- Display Animated History -----------------
def display_animated_history():
    if "history" not in st.session_state or not st.session_state.history:
        return

    st.markdown('<h3 class="neon-subtitle">📝 History</h3>', unsafe_allow_html=True)

    # Each history entry animated like cyberpunk terminal
    for idx, item in enumerate(reversed(st.session_state.history)):
        st.markdown(f"""
        <div class="glass-card history-card">
            <p class="animated-text" style="--delay:{idx*0.5}s;"><strong>Message:</strong> {item['Message']}</p>
            <p class="animated-text" style="--delay:{idx*0.5 + 0.2}s;"><strong>Prediction:</strong> {item['Prediction']}</p>
            <p class="animated-text" style="--delay:{idx*0.5 + 0.4}s;"><strong>Confidence:</strong> {item['Confidence']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- Spam Checker -----------------
def spam_checker_app():
    st.markdown('<h1 class="neon-title">🛑 Spam / Scam Checker</h1>', unsafe_allow_html=True)
    st.markdown('<p class="neon-subtitle">✉️ Enter your message below to detect SPAM or SCAM.</p>', unsafe_allow_html=True)

    text = st.text_area("", height=150, placeholder="Type or paste your message here...")

    if st.button("⚡ Check Spam"):
        if not text.strip():
            st.warning("⚠️ Please enter a message first!")
            return

        pipeline = load_pipeline("src/cyberthreatdetect/artifacts/scam_pipeline.pkl")
        if pipeline is None:
            return

        try:
            prediction = pipeline.predict([text])[0]
            probability = pipeline.predict_proba([text])[0][prediction]
            highlighted_message = highlight_keywords(text)

            # Output with glass card
            st.markdown(f"""
            <div class="glass-card output">
                <p>{highlighted_message}</p>
            </div>
            """, unsafe_allow_html=True)

            # Neon Alert
            if prediction == 1:
                st.markdown('<h2 class="neon-blink">🚨 SPAM/SCAM DETECTED!</h2>', unsafe_allow_html=True)
            else:
                st.markdown('<h2 class="neon-safe">✔ Not Spam</h2>', unsafe_allow_html=True)

            # Add to history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "Message": text,
                "Prediction": "SPAM" if prediction == 1 else "Not Spam",
                "Confidence": f"{probability*100:.2f}%"
            })

            # Display animated history
            display_animated_history()

            # Confidence chart
            st.markdown('<h3 class="neon-subtitle">📊 Confidence</h3>', unsafe_allow_html=True)
            st.bar_chart(pd.DataFrame({"Confidence": [probability*100]}))

        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ----------------- Cybersecurity Tips -----------------
def cybersecurity_tips():
    st.markdown('<h1 class="neon-title">💡 Cybersecurity Tips</h1>', unsafe_allow_html=True)

    tips = [
        "🔒 Use strong and unique passwords for each account.",
        "📧 Do not click on suspicious links or download unknown attachments.",
        "🛡 Keep your software and antivirus updated.",
        "🧑‍💻 Enable two-factor authentication wherever possible.",
        "🌐 Use secure networks and avoid public Wi-Fi for sensitive transactions.",
        "💾 Backup important data regularly.",
        "⚠️ Be cautious of phishing attempts in emails and messages.",
        "📝 Monitor your accounts for unusual activity.",
    ]

    for tip in tips:
        st.markdown(f'<p class="neon-tip">{tip}</p>', unsafe_allow_html=True)

# ----------------- Cyberpunk CSS -----------------
st.markdown("""
<style>
html, body, .stApp { 
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364); 
    color: #e0e0e0; 
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Glass Cards */
.glass-card {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 20px;
    padding: 20px;
    border: 1px solid rgba(0,255,204,0.5);
    box-shadow: 0 0 20px rgba(0,255,204,0.2);
    backdrop-filter: blur(10px);
    margin-bottom: 20px;
}

/* Glass History Cards */
.glass-card.history-card {
    background: rgba(0,0,0,0.25);
    border: 1px solid rgba(0,255,204,0.5);
    border-radius: 15px;
    padding: 12px 15px;
    margin-bottom: 10px;
    box-shadow: 0 0 15px rgba(0,255,204,0.2);
    backdrop-filter: blur(8px);
    font-size: 0.95em;
    color: #00ffcc;
}
.glass-card.history-card p { margin: 3px 0; }

/* Neon Buttons */
div.stButton > button:first-child {
    background: linear-gradient(45deg, #00ffcc, #00aaff);
    color: black; font-weight: bold; font-size: 18px; border-radius: 12px;
    padding: 10px 25px; transition: 0.3s ease;
}
div.stButton > button:first-child:hover {
    transform: scale(1.08); box-shadow: 0 0 20px #00ffcc;
}

/* Neon Titles */
.neon-title {
    color: #00ffcc; font-size: 2.8em; font-weight: bold; text-align: center;
    text-shadow: 0 0 5px #00ffcc, 0 0 10px #00ffcc, 0 0 20px #00ffcc;
}
.neon-subtitle {
    color: #ff6ec7; font-size: 1.4em; font-weight: bold; text-align: center;
    text-shadow: 0 0 5px #ff6ec7, 0 0 10px #ff6ec7;
}
.neon-blink {
    color: #ff0000; text-align: center; font-size: 2.2em; font-weight: bold;
    text-shadow: 0 0 10px #ff0000, 0 0 20px #ff0000, 0 0 30px #ff0000;
    animation: blink-animation 1s infinite;
}
.neon-safe {
    color: #00ff7f; text-align: center; font-size: 2.2em; font-weight: bold;
    text-shadow: 0 0 10px #00ff7f, 0 0 20px #00ff7f;
}
.neon-keyword {
    color: #ff4d6d;
    text-shadow: 0 0 8px #ff4d6d, 0 0 15px #00ffcc;
    animation: glowKeyword 1.2s infinite alternate;
}
@keyframes glowKeyword { 0% { text-shadow: 0 0 5px #ff4d6d; } 50% { text-shadow: 0 0 15px #ff4d6d, 0 0 20px #00ffcc; } 100% { text-shadow: 0 0 5px #ff4d6d; } }

.neon-tip {
    color: #00ffff; font-size: 1.2em; margin-left: 20px; margin-bottom: 8px;
    text-shadow: 0 0 5px #00ffff, 0 0 10px #ff00ff;
    animation: pulseTip 2s infinite alternate;
}

/* Animated text for history */
.animated-text {
    opacity: 0;
    color: #00ffcc;
    text-shadow: 0 0 5px #00ffcc, 0 0 10px #ff4d6d;
    animation: fadeIn 0.8s forwards;
    animation-delay: var(--delay);
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateX(-10px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes blink-animation { 0% {opacity: 1;} 50% {opacity: 0.2;} 100% {opacity: 1;} }
@keyframes pulseTip { 0% {text-shadow:0 0 5px #00ffff;} 100% {text-shadow:0 0 20px #ff00ff;} }
</style>
""", unsafe_allow_html=True)

# ----------------- Sidebar -----------------
st.sidebar.title("🛡️ Cyber Threat Detection")
module = st.sidebar.selectbox("Select Module", ["Spam Checker", "Cybersecurity Tips"])

if module == "Spam Checker":
    spam_checker_app()
elif module == "Cybersecurity Tips":
    cybersecurity_tips()