import imaplib
import email
import re
import os
from datetime import datetime, timedelta

IMAP_HOST = "imap.gmail.com"
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

DAYS_BACK = 10


def extract_failed_email(text):
    """
    Extract failed recipient from bounce message
    """
    patterns = [
        r"Final-Recipient: rfc822;(.+)",
        r"Original-Recipient: rfc822;(.+)",
        r"To:\s*(\S+@\S+)"
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()

    return None


def is_bounce(msg):
    """
    Detect bounce emails
    """
    from_addr = (msg.get("From") or "").lower()
    subject = (msg.get("Subject") or "").lower()
    content_type = (msg.get("Content-Type") or "").lower()

    if "mailer-daemon" in from_addr:
        return True
    if "delivery status notification" in subject:
        return True
    if "undelivered" in subject or "mail delivery failed" in subject:
        return True
    if "multipart/report" in content_type:
        return True

    return False


def main():
    since_date = (datetime.utcnow() - timedelta(days=DAYS_BACK)).strftime("%d-%b-%Y")
    print(f"Checking bounces since {since_date}")

    mail = imaplib.IMAP4_SSL(IMAP_HOST)
    mail.login(EMAIL_USER, EMAIL_PASS)
    mail.select("INBOX")

    status, messages = mail.search(None, f'(SINCE "{since_date}")')

    bounced_emails = set()

    for num in messages[0].split():
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        if not is_bounce(msg):
            continue

        payload = msg.as_string()
        failed_email = extract_failed_email(payload)

        if failed_email:
            bounced_emails.add(failed_email)
            print(f"❌ Bounce detected: {failed_email}")

    if not bounced_emails:
        print("✅ No bounces found")

    mail.logout()


if __name__ == "__main__":
    main()
