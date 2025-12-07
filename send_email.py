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

emails_df = pd.read_csv("emails.csv")

if os.path.exists("sent_log.csv"):
    sent_df = pd.read_csv("sent_log.csv")
    sent_emails = set(sent_df["email"].tolist())
else:
    sent_emails = set()
    pd.DataFrame(columns=["email"]).to_csv("sent_log.csv", index=False)

pending_df = emails_df[~emails_df["email"].isin(sent_emails)]

LIMIT = 125
MIN_DELAY = 50
MAX_DELAY = 120

SUBJECTS = [
    "Application for Python/Backend Developer Role",
    "Exploring Python Backend Opportunities",
    "Regarding Python Backend Position",
    "Interest in Python Developer Openings",
    "Application: Python Backend Engineer",
    "Inquiry About Python Developer Roles",
    "Potential Fit for Python Backend Position",
    "Profile for Python/Backend Developer"
]

OPENINGS = [
    "I hope you're doing well.",
    "Hope you're having a great day.",
    "Hope you're doing great.",
    "I hope everything is going well on your end.",
    "Hope you're staying productive and healthy.",
    "Trust you're doing well.",
    "Hope this message finds you well.",
    "I appreciate you taking a moment to read this.",
    "Thank you for your time.",
    "Hope you're having a productive week."
]

SIGNATURES = [
    "Best regards,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Warm regards,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Sincerely,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Thank you,\nAnkush Singh Gandhi\n+91-95296-39652",
    "Best,\nAnkush\n+91-95296-39652",
    "Regards,\nAnkush\n+91-95296-39652",
]

LINKS = "\nhttps://warriorwhocodes.com\nhttps://www.linkedin.com/in/ankushsinghgandhi"

ATTACHMENT_PATH = "resume.pdf"


def generate_email_body(first_name):
    opening = random.choice(OPENINGS)
    signature = random.choice(SIGNATURES)

    body = f"""
Hi {first_name},

{opening}

I’m reaching out to explore opportunities for Python Backend roles within your organization or network. 
I have 2+ years of experience working with Flask, Django, REST APIs, MySQL, MongoDB, Redis, and cloud deployments — 
with strong focus on scalable backend systems and performance optimization.

I understand you may not be hiring immediately, but I would appreciate the opportunity to connect or 
be considered for future openings. I genuinely believe my backend engineering experience can be a strong fit 
for fast-growing teams.

Thank you for your time. Happy to provide any additional information.

{signature}
{LINKS}
"""
    return body


def send_email(to_email, first_name):
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = to_email
    msg["Subject"] = random.choice(SUBJECTS)

    body_text = generate_email_body(first_name)
    msg.attach(MIMEText(body_text, "plain"))

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
