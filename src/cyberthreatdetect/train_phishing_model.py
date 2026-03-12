from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
from pathlib import Path
st.markdown("""
<style>

html, body, .stApp {
    height: 100%;
    margin: 0;
    padding: 0;
    background: radial-gradient(circle at top left, #0f0f0f, #1b1b1b, #000000) !important;
}

/* Hacker grid overlay */
.stApp::before {
    content: "";
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(#00ff00 1px, transparent 1px),
        linear-gradient(90deg, #00ff00 1px, transparent 1px);
    background-size: 45px 45px;
    opacity: 0.08;
    z-index: -1;
    pointer-events: none;
}

</style>
""", unsafe_allow_html=True)

def train():
    data = [
        ("Your PayPal account will be suspended. Verify immediately.", 1),
        ("Your Amazon order has been shipped.", 0),
        ("Unusual login detected. Confirm your identity.", 1),
        ("Your monthly bank statement is ready.", 0),
        ("Click this link to update your password.", 1),
        ("Your package will arrive tomorrow.", 0),
    ]

    df = pd.DataFrame(data, columns=["text", "label"])

    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["text"])
    y = df["label"]

    model = LogisticRegression()
    model.fit(X, y)

    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    joblib.dump(model, artifacts / "phishing_model.pkl")
    joblib.dump(vectorizer, artifacts / "vectorizer.pkl")

    print("Model saved to artifacts/phishing_model.pkl")
    print("Vectorizer saved to artifacts/vectorizer.pkl")

if __name__ == "__main__":
    train()