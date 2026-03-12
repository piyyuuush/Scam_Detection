import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib
from pathlib import Path

def train():
    # Sample dataset of scam vs safe messages
    data = [
        ("You won a $1000 gift card! Click here to claim.", 1),
        ("Your bank account has unusual activity. Verify now.", 1),
        ("Congratulations! You are selected for a prize.", 1),
        ("Please send your OTP to receive your reward.", 1),
        ("Your Amazon order has been shipped.", 0),
        ("Your package will arrive tomorrow.", 0),
        ("Meeting scheduled for 10 AM tomorrow.", 0),
        ("Monthly report is ready for download.", 0),
    ]

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=["text", "label"])

    # Vectorize text
    vectorizer = TfidfVectorizer(stop_words="english")
    X = vectorizer.fit_transform(df["text"])
    y = df["label"]

    # Train Logistic Regression model
    model = LogisticRegression()
    model.fit(X, y)

    # Save artifacts
    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)

    joblib.dump(model, artifacts / "scam_model.pkl")
    joblib.dump(vectorizer, artifacts / "vectorizer.pkl")

    print("Model saved to artifacts/scam_model.pkl")
    print("Vectorizer saved to artifacts/vectorizer.pkl")

if __name__ == "__main__":
    train()