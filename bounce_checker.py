import imaplib
import email
import os
import re
import csv
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
IMAP_HOST = "imap.gmail.com"
EMAIL_USER = os.environ["EMAIL_ADDRESS"]
EMAIL_PASS = os.environ["EMAIL_PASSWORD"]

SENT_LOG_CSV = "sent_log.csv"
BOUNCED_CSV = "bounced_emails.csv"

DAYS_BACK = 20
# ----------------------------------------


def load_sent_emails():
    if not os.path.exists(SENT_LOG_CSV):
        raise FileNotFoundError("sent_log.csv not found")

    with open(SENT_LOG_CSV, newline="") as f:
        reader = csv.DictReader(f)
        return {row["email"].strip().lower() for row in reader}


def load_existing_bounces():
    if not os.path.exists(BOUNCED_CSV):
        return set()

    with open(BOUNCED_CSV, newline="") as f:
        reader = csv.DictReader(f)
        return {row["email"].strip().lower() for row in reader}


def append_bounce(email_id, bounce_type):
    file_exists = os.path.exists(BOUNCED_CSV)

    with open(BOUNCED_CSV, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["email", "bounce_type", "detected_on"])

        writer.writerow([
            email_id,
            bounce_type,
            datetime.utcnow().strftime("%Y-%m-%d")
        ])


def extract_failed_email(text):
    patterns = [
        r"Final-Recipient: rfc822;(.+)",
        r"Original-Recipient: rfc822;(.+)",
        r"Your message wasn't delivered to\s+(\S+@\S+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip().lower()

    return None


def detect_bounce_type(text):
    text = text.lower()
    if re.search(r"5\.\d\.\d|address not found|user unknown|no such user", text):
        return "hard"
    if re.search(r"4\.\d\.\d|mailbox full|temporarily|try again later", text):
        return "soft"
    return "unknown"


def is_bounce(msg):
    from_addr = (msg.get("From") or "").lower()
    subject = (msg.get("Subject") or "").lower()
    content_type = (msg.get("Content-Type") or "").lower()

    return (
        "mailer-daemon" in from_addr
        or "delivery status notification" in subject
        or "undelivered" in subject
        or "multipart/report" in content_type
    )


def main():
    since_date = (datetime.utcnow() - timedelta(days=DAYS_BACK)).strftime("%d-%b-%Y")
    print(f"🔍 Checking bounces since {since_date}")

    sent_emails = load_sent_emails()
    existing_bounces = load_existing_bounces()

    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(EMAIL_USER, EMAIL_PASS)

    # IMPORTANT: Scan ALL MAIL (Inbox + Spam)
    mail.select('"[Gmail]/All Mail"')

    status, messages = mail.search(None, f'(SINCE "{since_date}")')

    new_bounces = 0

    for num in messages[0].split():
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        if not is_bounce(msg):
            continue

        body = msg.as_string()
        failed_email = extract_failed_email(body)

        if not failed_email:
            continue

        if failed_email not in sent_emails:
            continue  # Ignore emails you never sent

        if failed_email in existing_bounces:
            continue  # Already recorded

        bounce_type = detect_bounce_type(body)
        append_bounce(failed_email, bounce_type)

        existing_bounces.add(failed_email)
        new_bounces += 1

        print(f"❌ {bounce_type.upper()} bounce detected: {failed_email}")

    if new_bounces == 0:
        print("✅ No new bounces found")

    mail.logout()


if __name__ == "__main__":
    main()
