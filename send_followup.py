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

print(f"Follow-up emails to send today: {len(pending_followup)}")

FOLLOWUP_LIMIT = 40
MIN_DELAY = 40
MAX_DELAY = 60

SUBJECT_OPTIONS = [
    "Following up on my previous email",
    "Quick follow-up on my application",
    "Checking in regarding my earlier message",
    "Just circling back on my application",
    "Wanted to follow up on my previous note",
]

OPENERS = [
    "Hope you’re doing well.",
    "Hope your day is going great.",
    "I hope you're having a productive week.",
    "Hope everything is going smoothly on your side.",
    "I hope you’re doing well and staying healthy.",
]

BODY_VARIANTS = [
    """
I wanted to quickly follow up on my earlier message regarding potential Python/Backend Developer opportunities.

I understand things can get busy, so I just wanted to check in and see if you had a chance to review my previous email. 
I’m still very interested in any backend roles involving Python, Django, Flask, REST APIs, or database work.

If you need any additional details from my side, I’d be happy to share them.
""",

    """
Just following up on my previous email about backend roles.  
I know schedules get packed, so I thought I’d circle back to see if you had a moment to review my application.

I remain excited about opportunities involving Python, API development, and scalable backend systems.
If there's anything more you need, feel free to let me know.
""",

    """
I'm checking in regarding my earlier note about Python backend opportunities.

I understand hiring timelines vary, so no rush — just wanted to ensure my previous email didn't get missed.  
I’m still very much interested and open to discussing how my experience in Python, Django, Flask, and databases aligns with your team’s needs.
""",

    """
Reaching out again to follow up on my previous message.

I know you receive many emails, so I wanted to check in politely. I’m still actively exploring opportunities that involve backend engineering, API development, and Python-based systems.
If there's any update or next step you'd recommend, I’d appreciate hearing from you.
"""
]

SIGNATURES = [
    """
Best regards,  
Ankush Singh Gandhi  
https://warriorwhocodes.com  
""",

    """
Warm regards,  
Ankush  
https://warriorwhocodes.com  
""",

    """
Thanks and regards,  
Ankush Singh  
https://warriorwhocodes.com  
""",

    """
Sincerely,  
Ankush  
Backend Developer  
https://warriorwhocodes.com  
""",
]

def build_email(first_name):
    subject = random.choice(SUBJECT_OPTIONS)
    opener = random.choice(OPENERS)
    body = random.choice(BODY_VARIANTS)
    signature = random.choice(SIGNATURES)

    final_body = f"Hi {first_name},\n\n{opener}\n{body}\n{signature}"
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
