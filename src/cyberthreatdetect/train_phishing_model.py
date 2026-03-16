import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# -------------------------------
# Load Dataset
# -------------------------------
df = pd.read_csv("services/datasets/phishing_url_dataset_10000.csv")

urls = df["url"]
labels = df["label"]


# -------------------------------
# URL Feature Extraction
# -------------------------------
def extract_features(url):

    return {
        "url_length": len(url),
        "has_https": 1 if "https" in url else 0,
        "has_ip": 1 if re.search(r"\d+\.\d+\.\d+\.\d+", url) else 0,
        "has_at": 1 if "@" in url else 0,
        "dot_count": url.count("."),
        "dash_count": url.count("-"),
        "slash_count": url.count("/"),
        "digit_count": sum(c.isdigit() for c in url),
    }


# -------------------------------
# Convert URLs → Features
# -------------------------------
features = [extract_features(u) for u in urls]

X = pd.DataFrame(features)
y = labels


# -------------------------------
# Train Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)


# -------------------------------
# Train Model
# -------------------------------
model = RandomForestClassifier(n_estimators=100)

model.fit(X_train, y_train)


# -------------------------------
# Accuracy
# -------------------------------
pred = model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, pred))


# -------------------------------
# Save Model
# -------------------------------
joblib.dump(model, "url_model.pkl")

print("✅ url_model.pkl created successfully")