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

LIMIT = 55       # emails/day
MIN_DELAY = 30   # minimum seconds between emails
MAX_DELAY = 45   # maximum seconds between emails

SUBJECT = "Application for Python/Backend Developer Position"

BODY = """
Hi {first_name},
I noticed that you are currently hiring for Python roles, and I wanted to reach out directly. With 2+ years of experience as Python Backend Developer, I am confident in my ability to contribute effectively to your team and believe my skills in building scalable systems using Flask, Django, REST APIs, and SQL/NoSQL databases (MySQL, MongoDB, Redis) align well with the requirements of the role.

What excites me most is the chance to bring this mix of backend expertise, cloud deployment, and real-time data experience to opportunities your team is hiring for. I’d love to connect and share my resume for your consideration.

Thank you for considering my application. I have attached my resume for your review. I would welcome the opportunity to discuss how my background, skills, and passion for building scalable backend systems make me a strong candidate for this position.

I look forward to hearing from you soon.

Best regards,
Ankush Singh Gandhi
+91-95296-39652
[https://warriorwhocodes.com](https://warriorwhocodes.com)
[https://www.linkedin.com/in/ankushsinghgandhi](https://www.linkedin.com/in/ankushsinghgandhi)
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
