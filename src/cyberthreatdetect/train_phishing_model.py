import pandas as pd
import joblib
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# -----------------------------
# Load Dataset
# -----------------------------

df = pd.read_csv("phishing_dataset_10000.csv")

print("Dataset shape:", df.shape)

X = df["text"]
y = df["label"]

# -----------------------------
# Train Test Split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# Text Vectorization
# -----------------------------

vectorizer = TfidfVectorizer(
    stop_words="english",
    max_features=5000
)

X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

# -----------------------------
# Train Model
# -----------------------------

model = LogisticRegression(max_iter=1000)

model.fit(X_train_vec, y_train)

# -----------------------------
# Evaluate Model
# -----------------------------

pred = model.predict(X_test_vec)

accuracy = accuracy_score(y_test, pred)

print("Accuracy:", accuracy)

print("\nClassification Report:\n")
print(classification_report(y_test, pred))

# -----------------------------
# Save Model
# -----------------------------

artifacts = Path("artifacts")
artifacts.mkdir(exist_ok=True)

joblib.dump(model, artifacts / "phishing_model.pkl")
joblib.dump(vectorizer, artifacts / "vectorizer.pkl")

print("\nModel saved in artifacts folder")