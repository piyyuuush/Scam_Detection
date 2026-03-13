import streamlit as st
import joblib
import re
from pathlib import Path

# ----------------- Light Theme CSS with Animations -----------------
st.markdown("""
<style>
.light-card {
    background: #F5F5F5;
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.keyword-highlight {
    color: #d32f2f; /* red accent for spam words */
    font-weight: bold;
}

/* Safe message animation */
.safe-message {
    font-size: 1.5em;
    color: #4CAF50; /* green accent */
    font-weight: bold;
    animation: fadeIn 1.5s ease-in-out;
}

/* Spam message animation */
.spam-message {
    font-size: 1.5em;
    color: #d32f2f; /* red accent */
    font-weight: bold;
    animation: pulseAlert 1s infinite alternate;
}

/* Keyframes */
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulseAlert {
    from { text-shadow: 0 0 5px #d32f2f; }
    to   { text-shadow: 0 0 20px #d32f2f; }
}
</style>
""", unsafe_allow_html=True)

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
            f"<span class='keyword-highlight'>{kw}</span>",
            highlighted
        )
    return highlighted

# ----------------- Display History -----------------
def display_history():
    if "history" not in st.session_state or not st.session_state.history:
        return

    st.subheader("📝 History")
    for item in reversed(st.session_state.history):
        st.markdown(f"""
        <div class="light-card">
            <p><strong>Message:</strong> {item['Message']}</p>
            <p><strong>Prediction:</strong> {item['Prediction']}</p>
            <p><strong>Confidence:</strong> {item['Confidence']}</p>
        </div>
        """, unsafe_allow_html=True)

# ----------------- Spam Checker -----------------
def spam_checker_app():
    st.title("🛑 Spam / Scam Checker")
    st.write("✉️ Enter your message below to detect SPAM or SCAM.")

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

            if hasattr(pipeline, "classes_"):
                idx = list(pipeline.classes_).index(prediction)
                probability = proba[idx]
            else:
                probability = max(proba)

            highlighted_message = highlight_keywords(text)
            st.markdown(f"<div class='light-card'>{highlighted_message}</div>", unsafe_allow_html=True)

            if prediction == 1:
                st.markdown('<div class="spam-message">🚨 SPAM/SCAM DETECTED!</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="safe-message">✔ Not Spam</div>', unsafe_allow_html=True)

            # Save to history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "Message": text,
                "Prediction": "SPAM" if prediction == 1 else "Not Spam",
                "Confidence": f"{probability*100:.2f}%"
            })

            display_history()
            st.metric("Confidence", f"{probability*100:.2f}%")

        except Exception as e:
            st.error(f"Prediction failed: {e}")

# ----------------- Sidebar -----------------
st.sidebar.title("🛡️ Cyber Threat Detection")
module = st.sidebar.selectbox("Select Module", ["Spam Checker", "Cybersecurity Tips"])

if module == "Spam Checker":
    spam_checker_app()
else:
    st.title("🔐 Cybersecurity Tips")
    st.write("Here you can add your tips content...")
