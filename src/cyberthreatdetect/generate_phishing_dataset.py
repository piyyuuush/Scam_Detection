import pandas as pd
import random

phishing_templates = [
"Your account has been suspended. Verify immediately.",
"Unusual login detected. Confirm your identity now.",
"Your bank account will be locked. Update details urgently.",
"You have won a prize. Click here to claim now.",
"Your PayPal account requires verification.",
"Your package delivery failed. Reschedule now.",
"Security alert! Reset your password immediately.",
"Your credit card has been blocked. Verify information.",
"Urgent: Confirm your payment information.",
"Your tax refund is ready. Submit details to receive."
]

safe_templates = [
"Your order has been shipped successfully.",
"Your bank statement is available.",
"Meeting scheduled for tomorrow.",
"Your subscription has been renewed.",
"Your payment was processed successfully.",
"Your flight ticket confirmation is attached.",
"Your monthly electricity bill is generated.",
"Your package will arrive tomorrow.",
"Your account password was updated successfully.",
"Your class schedule has been updated."
]

data = []

# Generate 5000 phishing messages
for i in range(5000):
    text = random.choice(phishing_templates)
    data.append((text, 1))

# Generate 5000 safe messages
for i in range(5000):
    text = random.choice(safe_templates)
    data.append((text, 0))

random.shuffle(data)

df = pd.DataFrame(data, columns=["text", "label"])

df.to_csv("phishing_dataset_10000.csv", index=False)

print("Dataset created successfully: phishing_dataset_10000.csv")