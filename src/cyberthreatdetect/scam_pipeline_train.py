# scam_pipeline_train.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pandas as pd
import joblib
from pathlib import Path

def train_pipeline():

    # Load your dataset (update filename here)
    df = pd.read_csv("spam.csv", encoding="latin1")

    # Rename columns to standard names
    df = df.rename(columns={"v1": "label", "v2": "text"})

    # Map labels: ham → 0, spam → 1
    df["label"] = df["label"].map({"ham": 0, "spam": 1})

    # Drop rows with missing text
    df = df.dropna(subset=["text"])

    # Create TF-IDF + Logistic Regression pipeline
    pipeline = make_pipeline(
        TfidfVectorizer(stop_words="english"),
        LogisticRegression(max_iter=1000)
    )

    # Train model
    pipeline.fit(df["text"], df["label"])

    # Save model
    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)
    joblib.dump(pipeline, artifacts / "scam_pipeline.pkl")

    print("Training completed.")
    print("Pipeline saved at artifacts/scam_pipeline.pkl")

if __name__ == "__main__":
    train_pipeline()