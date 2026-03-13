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
        highlighted = re.sub(f"(?i)\\b{kw}\\b", f"<span class='neon-keyword'>{kw}</span>", highlighted)
    return highlighted

# ----------------- Display History -----------------
def display_history():
    if "history" not in st.session_state or not st.session_state.history:
        return

    st.markdown('<h3 class="neon-subtitle">📝 History</h3>', unsafe_allow_html=True)

    for idx, item in enumerate(reversed(st.session_state.history)):
        st.markdown(f"""
        <div class="glass-card history-card">
            <p><strong>Message:</strong> {item['Message']}</p>
            <p><strong>Prediction:</strong> {item['Prediction']}</p>
            <p><strong>Confidence:</strong> {item['Confidence']}</p>
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
            proba = pipeline.predict_proba([text])[0]

            # Fix probability selection based on class mapping
            if hasattr(pipeline, "classes_"):
                idx = list(pipeline.classes_).index(prediction)
                probability = proba[idx]
            else:
                probability = max(proba)

            highlighted_message = highlight_keywords(text)

            st.markdown(f"<div class='glass-card output'>{highlighted_message}</div>", unsafe_allow_html=True)

            if prediction == 1:
                st.markdown('<h2 class="neon-blink">🚨 SPAM/SCAM DETECTED!</h2>', unsafe_allow_html=True)
            else:
                # Inject CSS for safe message
                st.markdown("""
                <style>
                .stApp .neon-safe {
                    font-size: 2em;
                    text-align: left;
                    color: #00ff00;
                    text-shadow: 
                        0 0 5px #00ff00,
                        0 0 10px #00ff00,
                        0 0 20px #00ff00,
                        0 0 40px #00ff00;
                    animation: glowPulse 1.5s infinite alternate;
                }
                @keyframes glowPulse {
                    from { text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00; }
                    to   { text-shadow: 0 0 20px #00ff00, 0 0 40px #00ff00; }
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown('<h2 class="neon-safe">✔ Not Spam</h2>', unsafe_allow_html=True)

            # Save to history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "Message": text,
                "Prediction": "SPAM" if prediction == 1 else "Not Spam",
                "Confidence": f"{probability*100:.2f}%"
            })

            display_history()

            # Inject CSS for history + confidence section
            st.markdown("""
            <style>
            .stApp .neon-subtitle {
                font-size: 1.4em;
                text-align: left;
                color: #ff4d6d;
                text-shadow: 0 0 8px #ff4d6d;
                margin: 15px 0;
            }
            .stApp .glass-card.history-card {
                background: rgba(255,255,255,0.08);
                border-left: 4px solid #00ffff;
                border-radius: 12px;
                padding: 12px;
                margin: 8px 0;
                backdrop-filter: blur(8px);
                box-shadow: 0 4px 20px rgba(0,0,0,0.4);
                transition: transform 0.3s ease;
            }
            .stApp .glass-card.history-card:hover {
                transform: translateX(5px);
                box-shadow: 0 0 15px #00ffff;
            }
            .stApp .confidence-section {
                margin-top: 20px;
                padding: 12px;
                border-radius: 10px;
                background: rgba(255,255,255,0.05);
                box-shadow: 0 0 15px rgba(0,255,255,0.3);
            }
            </style>
            """, unsafe_allow_html=True)

            # Wrap chart in styled container
            st.markdown('<div class="confidence-section">', unsafe_allow_html=True)
            
            

        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ----------------- Cybersecurity Tips -----------------


# ----------------- Sidebar -----------------
st.sidebar.title("🛡️ Cyber Threat Detection")
module = st.sidebar.selectbox("Select Module", ["Spam Checker", "Cybersecurity Tips"])

if module == "Spam Checker":
    spam_checker_app()

