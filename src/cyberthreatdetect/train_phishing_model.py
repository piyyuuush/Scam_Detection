# phishing_model_safe_train.py
import pandas as pd
import re
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib
from pathlib import Path
import csv

# -----------------------------
# 1️⃣ Load CSV safely
# -----------------------------
csv_path = "phishing_dataset_10000.csv"  # replace with your CSV path

# Read in chunks to handle large files and skip malformed rows
chunks = pd.read_csv(
    csv_path,
    chunksize=50000,
    on_bad_lines='skip',       # skip lines with parsing errors
    quoting=csv.QUOTE_NONE,    # treat quotes as normal characters
    encoding='utf-8'
)

df = pd.concat(chunks, ignore_index=True)
print("✅ Dataset loaded successfully:", df.shape)
print(df.head())

# -----------------------------
# 2️⃣ Text preprocessing
# -----------------------------
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+|www\S+", " ", text)  # remove URLs
    text = re.sub(r"<.*?>", " ", text)           # remove HTML
    text = re.sub(r"[^a-z0-9\s]", " ", text)    # remove punctuation
    text = re.sub(r"\s+", " ", text)            # remove extra spaces
    return text.strip()

# -----------------------------
# 3️⃣ Combine Subject + Message
# -----------------------------
X = (df["Subject"].astype(str) + " " + df["Message"].astype(str)).apply(clean_text)

# Convert Spam/Ham to numeric labels
y = df["Spam/Ham"].apply(lambda x: 1 if str(x).lower() == "spam" else 0)

# -----------------------------
# 4️⃣ Train-test split
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# -----------------------------
# 5️⃣ Build pipeline
# -----------------------------
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1,2))),
    ("classifier", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# -----------------------------
# 6️⃣ Hyperparameter tuning (optional)
# -----------------------------
param_grid = {
    "classifier__C": [0.1, 1, 10],
    "tfidf__ngram_range": [(1,1), (1,2)]
}

grid = GridSearchCV(pipeline, param_grid, cv=3, scoring="f1", verbose=1)
grid.fit(X_train, y_train)

# -----------------------------
# 7️⃣ Evaluate model
# -----------------------------
y_pred = grid.predict(X_test)
print("\n✅ Best Params:", grid.best_params_)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# -----------------------------
# 8️⃣ Save trained model
# -----------------------------
artifacts = Path("artifacts")
artifacts.mkdir(exist_ok=True)
joblib.dump(grid.best_estimator_, artifacts / "phishing_email_model.pkl")
print("\n✅ Model saved at artifacts/phishing_email_model.pkl")

# -----------------------------
# 9️⃣ Real-time prediction function
# -----------------------------
def predict_email(subject, message):
    text = clean_text(f"{subject} {message}")
    model = joblib.load(artifacts / "phishing_email_model.pkl")
    pred = model.predict([text])[0]
    prob = model.predict_proba([text])[0]
    label = "Phishing/Spam (1)" if pred == 1 else "Legitimate/Ham (0)"
    confidence = max(prob) * 100
    return label, confidence

# Example usage
if __name__ == "__main__":
    sub = "Your account has unusual activity"
    msg = "Confirm your identity now or your account will be locked."
    label, conf = predict_email(sub, msg)
    print(f"\nPrediction: {label}, Confidence: {conf:.2f}%")