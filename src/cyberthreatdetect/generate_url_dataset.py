import pandas as pd
import random

safe_urls = [
    "https://google.com",
    "https://github.com",
    "https://facebook.com",
    "https://stackoverflow.com",
    "https://amazon.com",
    "https://microsoft.com",
    "https://apple.com",
    "https://wikipedia.org",
]

phishing_keywords = [
    "secure-login-update",
    "verify-account",
    "reset-password-now",
    "free-gift",
    "claim-prize",
    "paypal-security-alert",
    "bank-verification",
    "update-info-required",
    "urgent-action-needed",
    "lottery-winner",
]

data = []

for _ in range(5000):
    url = random.choice(safe_urls) + "/" + str(random.randint(1, 50000))
    data.append([url, 0])  # safe

for _ in range(5000):
    url = "http://" + random.choice(phishing_keywords) + str(random.randint(10, 9999)) + ".com"
    data.append([url, 1])  # phishing

df = pd.DataFrame(data, columns=["url", "label"])

df.to_csv("services/datasets/phishing_url_dataset_10000.csv", index=False)

print("Saved 10,000-row dataset successfully!")