import smtplib
import pandas as pd
import time
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

import email_config

EMAIL = email_config.EMAIL_ADDRESS
PASSWORD = email_config.EMAIL_PASSWORD

emails_df = pd.read_csv("emails.csv")

if os.path.exists("sent_log.csv"):
    sent_df = pd.read_csv("sent_log.csv")
    sent_emails = set(sent_df["email"].tolist())
else:
    sent_emails = set()
    pd.DataFrame(columns=["email"]).to_csv("sent_log.csv", index=False)

pending_df = emails_df[~emails_df["email"].isin(sent_emails)]

LIMIT = email_config.INITIAL_LIMIT
MIN_DELAY = email_config.INITIAL_MIN_DELAY
MAX_DELAY = email_config.INITIAL_MAX_DELAY


def generate_email_body(first_name):
    opening = random.choice(email_config.INITIAL_OPENINGS)
    signature = random.choice(email_config.INITIAL_SIGNATURES)

    body = email_config.INITIAL_BODY_TEMPLATE.format(
        first_name=first_name,
        opening=opening,
        signature=signature,
        links=email_config.LINKS
    )
    return body


def send_email(to_email, first_name):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = random.choice(email_config.INITIAL_SUBJECTS)

    body_text = generate_email_body(first_name)
    msg.attach(MIMEText(body_text, "plain"))

    with open(email_config.ATTACHMENT_PATH, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header("Content-Disposition", "attachment", filename="Resume.pdf")
        msg.attach(attach)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to_email, msg.as_string())
    server.quit()


count = 0

for _, row in pending_df.iterrows():
    if count >= LIMIT:
        break

    to_email = row["email"]
    first_name = row.get("first_name", "") or ""

    try:
        send_email(to_email, first_name)
        print(f"Sent: {to_email}")

        with open("sent_log.csv", "a") as log:
            log.write(f"{to_email}\n")

        count += 1

        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"Sleeping for {delay} seconds...")
        time.sleep(delay)

    except Exception as e:
        print(f"Failed: {to_email} - {e}")
        time.sleep(5)
