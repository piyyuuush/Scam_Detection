# scam_pipeline_train.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
import pandas as pd
import joblib
from pathlib import Path

def train_pipeline():
    # Sample data: 1 = spam/scam, 0 = not spam
    # scam_spam_dataset.py
# 1 = Spam/Scam, 0 = Not Spam
    data = [
    # Spam / Scam messages (label = 1)
    ("Congratulations! You won a $1000 gift card. Click here to claim.", 1),
    ("Your PayPal account has been limited. Verify immediately.", 1),
    ("Unusual login detected. Confirm your identity now.", 1),
    ("Click this link to update your password.", 1),
    ("You have received a package but need to pay customs fees.", 1),
    ("You are selected for a free iPhone! Claim it before the offer expires.", 1),
    ("Earn $5000 per week working from home. Limited spots!", 1),
    ("Your bank account will be closed unless you verify your details.", 1),
    ("Get a loan approved instantly, no credit check required.", 1),
    ("You have won a free vacation. Respond immediately.", 1),
    ("Urgent! Your account has been compromised. Reset your password.", 1),
    ("Act now! Limited time investment opportunity.", 1),
    ("You are a lucky winner! Claim your prize.", 1),
    ("Verify your mobile number to receive the reward.", 1),
    ("Your Netflix subscription is about to expire. Click to renew.", 1),
    ("Congratulations! You’ve been selected for a cash reward.", 1),
    ("Immediate action required to secure your account.", 1),
    ("You are eligible for a free gift card. Claim now.", 1),
    ("This is not a joke! Win $10,000 instantly.", 1),
    ("You have pending taxes. Pay now to avoid penalties.", 1),
    ("Click to download the free antivirus software.", 1),
    ("Your Facebook account has been suspended. Confirm now.", 1),
    ("Win a free car! Enter your details here.", 1),
    ("Get rich fast with this simple scheme.", 1),
    ("You have received a wire transfer. Confirm your account.", 1),
    ("Your account verification is pending. Click to complete.", 1),
    ("You have won a lottery! Claim your prize immediately.", 1),
    ("Confirm your identity to avoid account termination.", 1),
    ("Claim your free Amazon gift voucher now.", 1),
    ("Your credit card has suspicious charges. Verify now.", 1),
    ("Your phone number is selected for cash reward.", 1),
    ("Act fast! Free tickets to a concert. Claim now.", 1),
    ("You have a pending invoice. Pay immediately.", 1),
    ("Update your billing information to avoid service interruption.", 1),
    ("Your bank needs verification for security reasons.", 1),
    ("Free trial expired! Renew now to continue.", 1),
    ("You won a prize! Submit your details to claim.", 1),
    ("Your account has unusual activity. Confirm now.", 1),
    ("This is your final notice! Click to resolve.", 1),
    ("You have received $5000 from an unknown source.", 1),
    ("Confirm your subscription for free rewards.", 1),
    ("Immediate payment required for your overdue invoice.", 1),
    ("Claim your free cryptocurrency bonus now.", 1),
    ("Your mobile recharge failed. Click to retry.", 1),
    ("Special offer! Buy one get one free today.", 1),
    ("Congratulations! You have won a new car.", 1),
    ("Your account will be locked unless verified.", 1),
    ("Claim your reward points before they expire.", 1),
    ("Limited offer! Get 70% discount on your order.", 1),
    ("You are a winner! Click to redeem.", 1),
    
    # Non-Spam messages (label = 0)
    ("Your Amazon order has been shipped.", 0),
    ("Meeting scheduled tomorrow at 10 AM.", 0),
    ("Your monthly bank statement is ready.", 0),
    ("Your electricity bill for March is generated.", 0),
    ("Reminder: Doctor appointment at 4 PM today.", 0),
    ("Package will arrive tomorrow between 1-3 PM.", 0),
    ("Happy Birthday! Wishing you a wonderful day.", 0),
    ("Your subscription has been renewed successfully.", 0),
    ("Your flight booking is confirmed for next Monday.", 0),
    ("Your invoice for March has been emailed.", 0),
    ("Class timetable for this semester is uploaded.", 0),
    ("Your parcel tracking number is 123456.", 0),
    ("Your password was changed successfully.", 0),
    ("Your payment of $200 has been received.", 0),
    ("Event registration confirmed for April 20th.", 0),
    ("Your library books are due tomorrow.", 0),
    ("Your meeting room has been booked.", 0),
    ("Your gym membership has been renewed.", 0),
    ("Your order has been delivered.", 0),
    ("Your account balance is $1,500.", 0),
    ("Your package is ready for pickup.", 0),
    ("Your refund of $50 has been processed.", 0),
    ("Your online course enrollment is successful.", 0),
    ("Your car service appointment is confirmed.", 0),
    ("Your email subscription settings are updated.", 0),
    ("Your flight gate has changed to B12.", 0),
    ("Your hotel reservation is confirmed.", 0),
    ("Your Zoom meeting link is ready.", 0),
    ("Your insurance policy is renewed.", 0),
    ("Your lab test results are uploaded.", 0),
    ("Your order will be delivered tomorrow.", 0),
    ("Your school timetable has been updated.", 0),
    ("Your train ticket is booked.", 0),
    ("Your grocery order has been packed.", 0),
    ("Your electricity bill is paid.", 0),
    ("Your mobile recharge was successful.", 0),
    ("Your library account has been updated.", 0),
    ("Your flight boarding pass is ready.", 0),
    ("Your subscription for Netflix is active.", 0),
    ("Your doctor's appointment is scheduled.", 0),
    ("Your parcel has been dispatched.", 0),
    ("Your account statement is ready.", 0),
    ("Your course registration is confirmed.", 0),
    ("Your event ticket has been emailed.", 0),
    ("Your payment has been completed.", 0),
    ("Your car service reminder is set.", 0),
    ("Your parcel is arriving tomorrow.", 0),
    ("Your hotel booking is confirmed.", 0),
    ("Your Zoom meeting is scheduled.", 0),
    ("Your exam results have been published.", 0),
    ("Your bank transfer was successful.", 0),
    ("Your subscription payment has been received.", 0)
    ]
    df = pd.DataFrame(data, columns=["text", "label"])

    # Create pipeline: TF-IDF vectorizer + Logistic Regression
    pipeline = make_pipeline(
        TfidfVectorizer(stop_words="english"),
        LogisticRegression()
    )

    # Train the pipeline
    pipeline.fit(df["text"], df["label"])

    # Save the pipeline
    artifacts = Path("artifacts")
    artifacts.mkdir(exist_ok=True)
    joblib.dump(pipeline, artifacts / "scam_pipeline.pkl")
    print("Pipeline saved at artifacts/scam_pipeline.pkl")

if __name__ == "__main__":
    train_pipeline()