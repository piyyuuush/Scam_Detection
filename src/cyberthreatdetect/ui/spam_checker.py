import streamlit as st
import joblib
import re
import time
from pathlib import Path
import pandas as pd

def load_pipeline(path: str):
    p = Path(path)
    if not p.exists():
        st.error(f"❌ Pipeline file not found at {path}")
        return None
    return joblib.load(p)

SPAM_KEYWORDS = ["win","free","cash","gift","prize","urgent","click","verify",
                 "reward","congratulations","loan","account","limited","offer"]

def highlight_keywords(text):
    highlighted = text
    for kw in SPAM_KEYWORDS:
        highlighted = re.sub(f"(?i)\\b{kw}\\b", f"**{kw.upper()}**", highlighted)
    return highlighted

def display_history():
    if "history" not in st.session_state or not st.session_state.history:
        return
    st.subheader("📝 History")
    for item in reversed(st.session_state.history):
        st.info(f"**Message:** {item['Message']}\n\n"
                f"**Prediction:** {item['Prediction']}\n\n"
                f"**Confidence:** {item['Confidence']}")

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

            st.write(highlight_keywords(text))

            # Native attractive UI
            if prediction == 1:
                st.error("🚨 SPAM/SCAM DETECTED!")
            else:
                st.success("✔ Not Spam")

            # Animated confidence bar
            st.write("Confidence level:")
            progress = st.progress(0)
            for i in range(int(probability*100)):
                progress.progress(i+1)
                time.sleep(0.01)

            # Metric
            st.metric("Confidence", f"{probability*100:.2f}%")

            # Save history
            if "history" not in st.session_state:
                st.session_state.history = []
            st.session_state.history.append({
                "Message": text,
                "Prediction": "SPAM" if prediction == 1 else "Not Spam",
                "Confidence": f"{probability*100:.2f}%"
            })

            display_history()

            # Probability chart
            st.subheader("📊 Probability Breakdown")
            df = pd.DataFrame({"Class": pipeline.classes_, "Probability": proba})
            st.bar_chart(df.set_index("Class"))

        except Exception as e:
            st.error(f"Prediction failed: {e}")

st.sidebar.title("🛡️ Cyber Threat Detection")
module = st.sidebar.selectbox("Select Module", ["Spam Checker", "Cybersecurity Tips"])

if module == "Spam Checker":
    spam_checker_app()
else:
    st.title("🔐 Cybersecurity Tips")
    st.write("Here you can add your tips content...")
