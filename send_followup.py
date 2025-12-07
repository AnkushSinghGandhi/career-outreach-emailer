import smtplib
import pandas as pd
import time
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

EMAIL = os.environ["EMAIL_ADDRESS"]
PASSWORD = os.environ["EMAIL_PASSWORD"]

emails_df = pd.read_csv("emails.csv")
sent_df = pd.read_csv("sent_log.csv")
replied_df = pd.read_csv("replied.csv") if os.path.exists("replied.csv") else pd.DataFrame(columns=["email"])
followup_df = pd.read_csv("followup_sent.csv") if os.path.exists("followup_sent.csv") else pd.DataFrame(columns=["email"])

sent_emails = set(sent_df["email"].tolist())
replied_emails = set(replied_df["email"].tolist())
followed_emails = set(followup_df["email"].tolist())

pending_followup = [email for email in sent_emails if email not in replied_emails and email not in followed_emails]

print(f"Follow-up emails to send: {len(pending_followup)}")

SUBJECT = "Following Up On My Previous Application"

BODY = """
Hi {first_name},

I wanted to follow up on my previous message regarding Python/Backend Developer opportunities.

I understand things get busy, so I’m just checking in to see if you had a chance to review my application. 
I remain very interested in roles involving Python, Flask, Django, REST APIs, MySQL/MongoDB, and backend engineering.

If you need any additional information, I’ll be happy to provide it.

Thank you for your time!

Best regards,
Ankush Singh Gandhi
https://warriorwhocodes.com
"""

def send_email(to_email, first_name):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(BODY.format(first_name=first_name), "plain"))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to_email, msg.as_string())
    server.quit()

for email in pending_followup:
    row = emails_df[emails_df["email"] == email]
    first_name = row["first_name"].iloc[0] if "first_name" in row and len(row) > 0 else ""

    try:
        send_email(email, first_name)
        print(f"Follow-up sent: {email}")

        new_entry = pd.DataFrame([[email]], columns=["email"])
        new_entry.to_csv("followup_sent.csv", mode="a", header=False, index=False)

        delay = random.randint(20, 40)
        print(f"Sleeping for {delay} seconds...")
        time.sleep(delay)

    except Exception as e:
        print(f"Failed to send follow-up to {email}: {e}")
        time.sleep(5)
