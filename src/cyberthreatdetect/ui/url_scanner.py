import streamlit as st
import pandas as pd
import re
import joblib
from pathlib import Path

# -----------------------------
# Load Model
# -----------------------------
MODEL_PATH = Path("src/cyberthreatdetect/artifacts/url_model.pkl")

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

model = load_model()

# -----------------------------
# Feature Extraction
# -----------------------------
def extract_features(url):

    features = {
        "url_length": len(url),
        "has_https": 1 if "https" in url else 0,
        "has_ip": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        "has_at": 1 if "@" in url else 0,
        "dot_count": url.count("."),
        "dash_count": url.count("-"),
        "slash_count": url.count("/"),
        "digit_count": sum(c.isdigit() for c in url),
    }

    return pd.DataFrame([features])


# -----------------------------
# UI
# -----------------------------
def url_scanner_app():

    st.title("🔗 URL Phishing Scanner")
    st.write("Scan a website link to check if it is **Safe or Phishing**.")

    url = st.text_input("Enter URL to scan")

    if st.button("Scan URL"):

        if url.strip() == "":
            st.warning("Please enter a URL")
            return

        # Extract features
        features = extract_features(url)

        # Predict
        prediction = model.predict(features)[0]
        probability = model.predict_proba(features)[0][1]

        st.subheader("🔎 Scan Result")

        if prediction == 1:
            st.error("⚠ Phishing URL Detected")
        else:
            st.success("✅ Safe URL")

        st.write(f"Confidence Score: **{round(probability*100,2)}%**")

        # Show extracted features
        with st.expander("View Extracted Features"):
            st.dataframe(features)


# -----------------------------
# Run Standalone
# -----------------------------
if __name__ == "__main__":
    url_scanner_app()