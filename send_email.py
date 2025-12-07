import smtplib
import pandas as pd
import time
import os
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

EMAIL = os.environ["EMAIL_ADDRESS"]
PASSWORD = os.environ["EMAIL_PASSWORD"]

# Load master email list
emails_df = pd.read_csv("emails.csv")

# Load sent log (or create if missing)
if os.path.exists("sent_log.csv"):
    sent_df = pd.read_csv("sent_log.csv")
    sent_emails = set(sent_df["email"].tolist())
else:
    sent_emails = set()
    pd.DataFrame(columns=["email"]).to_csv("sent_log.csv", index=False)

# Filter only new emails
pending_df = emails_df[~emails_df["email"].isin(sent_emails)]

LIMIT = 125       # emails/day
MIN_DELAY = 30   # minimum seconds between emails
MAX_DELAY = 45   # maximum seconds between emails

SUBJECT = "Application for Python/Backend Developer Position"

BODY = """
Hi {first_name}

I hope you're doing well.

I’m reaching out to express my interest in exploring any current or upcoming opportunities for Python Backend roles within your organization or network. I have 2+ years of experience working with Flask, Django, REST APIs, and databases such as MySQL, MongoDB, and Redis, along with hands-on experience in building scalable backend systems and deploying cloud-based applications.

I understand you may not be actively hiring at the moment, but I would appreciate the chance to connect and share my resume for future consideration. I’m confident that my background in backend development, system design, and performance optimization aligns well with the needs of high-growth engineering teams.

Thank you for your time, and please let me know if I can provide any additional information.
I look forward to staying connected.

Best regards,
Ankush Singh Gandhi
+91-95296-39652
https://warriorwhocodes.com
https://www.linkedin.com/in/ankushsinghgandhi
"""

ATTACHMENT_PATH = "resume.pdf"

def send_email(to_email, first_name):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = SUBJECT

    msg.attach(MIMEText(BODY.format(first_name=first_name), "plain"))

    with open(ATTACHMENT_PATH, "rb") as f:
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
    first_name = row.get("first_name", "")

    try:
        send_email(to_email, first_name)
        print(f"Sent: {to_email}")

        # Log as sent
        with open("sent_log.csv", "a") as log:
            log.write(f"{to_email}\n")

        count += 1

        # Random delay between MIN_DELAY and MAX_DELAY seconds
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        print(f"Sleeping for {delay} seconds...")
        time.sleep(delay)

    except Exception as e:
        print(f"Failed: {to_email} - {e}")
        time.sleep(5)
