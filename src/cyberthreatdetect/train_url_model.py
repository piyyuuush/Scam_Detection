import pandas as pd
import re
import joblib
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

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
# Example Dataset
# -------------------------------
urls = [
    "https://google.com",
    "https://github.com",
    "https://amazon.in",
    "http://192.168.1.1/login",
    "http://paypal@verify-login.com",
    "http://free-money-prize.xyz",
    "https://facebook.com",
    "https://stackoverflow.com",
    "http://secure-update-account.net",
    "http://login-bank-security.com"
]

labels = [
    0,0,0,1,1,1,0,0,1,1
]  # 0 = safe, 1 = phishing

# -------------------------------
# Feature Engineering
# -------------------------------
features = [extract_features(u) for u in urls]

X = pd.DataFrame(features)
y = labels

# -------------------------------
# Train Model
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

# -------------------------------
# Accuracy Check
# -------------------------------
pred = model.predict(X_test)
print("Accuracy:", accuracy_score(y_test, pred))

# -------------------------------
# Save Model
# -------------------------------
joblib.dump(model, "url_model.pkl")

print("✅ url_model.pkl created successfully")