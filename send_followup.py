import smtplib
import pandas as pd
import time
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import email_config

EMAIL = email_config.EMAIL_ADDRESS
PASSWORD = email_config.EMAIL_PASSWORD

emails_df = pd.read_csv("emails.csv")
sent_df = pd.read_csv("sent_log.csv")
replied_df = pd.read_csv("replied.csv") if os.path.exists("replied.csv") else pd.DataFrame(columns=["email"])
followup_df = pd.read_csv("followup_sent.csv") if os.path.exists("followup_sent.csv") else pd.DataFrame(columns=["email"])

sent_emails = set(sent_df["email"].tolist())
replied_emails = set(replied_df["email"].tolist())
followed_emails = set(followup_df["email"].tolist())

pending_followup = [email for email in sent_emails if email not in replied_emails and email not in followed_emails]

print(f"Follow-up emails to send today: {len(pending_followup)}")

FOLLOWUP_LIMIT = email_config.FOLLOWUP_LIMIT
MIN_DELAY = email_config.FOLLOWUP_MIN_DELAY
MAX_DELAY = email_config.FOLLOWUP_MAX_DELAY


def build_email(first_name):
    subject = random.choice(email_config.FOLLOWUP_SUBJECTS)
    opener = random.choice(email_config.FOLLOWUP_OPENERS)
    body = random.choice(email_config.FOLLOWUP_BODY_VARIANTS)
    signature = random.choice(email_config.FOLLOWUP_SIGNATURES)

    final_body = email_config.FOLLOWUP_BODY_TEMPLATE.format(
        first_name=first_name,
        opener=opener,
        body=body,
        signature=signature
    )
    return subject, final_body


def send_email(to_email, first_name):
    subject, full_body = build_email(first_name)

    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(full_body, "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to_email, msg.as_string())
    server.quit()


count = 0

for email in pending_followup:
    if count >= FOLLOWUP_LIMIT:
        print("Follow-up limit reached.")
        break

    row = emails_df[emails_df["email"] == email]
    first_name = row["first_name"].iloc[0] if "first_name" in row and len(row) > 0 else ""

    try:
        send_email(email, first_name)
        print(f"Follow-up sent: {email}")

        pd.DataFrame([[email]], columns=["email"]).to_csv("followup_sent.csv", mode="a", header=False, index=False)

        count += 1

        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"Sleeping for {delay} seconds...")
        time.sleep(delay)

    except Exception as e:
        print(f"Failed to send follow-up to {email}: {e}")
        time.sleep(5)
