import imaplib
import email
import os
import re
import csv
import email_config
import mailer
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
IMAP_HOST = "imap.gmail.com"
EMAIL_USER = email_config.EMAIL_ADDRESS
EMAIL_PASS = email_config.EMAIL_PASSWORD

SENT_LOG_CSV = "sent_log.csv"
BOUNCED_CSV = "bounced_emails.csv"

DAYS_BACK = email_config.CHECK_DAYS_BACK
# ----------------------------------------

logger = mailer.logger

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

def process_folder(mail, folder_name, since_date, sent_emails, existing_bounces):
    logger.info(f"Scanning folder: {folder_name}")
    mail.select(f'"{folder_name}"')
    
    status, messages = mail.search(None, f'(SINCE "{since_date}")')
    new_bounces = 0

    if status != "OK":
        logger.warning(f"Could not search folder {folder_name}")
        return 0

    for num in messages[0].split():
        _, data = mail.fetch(num, "(RFC822)")
        msg = email.message_from_bytes(data[0][1])

        if not is_bounce(msg):
            continue

        body = msg.as_string()
        failed_email = extract_failed_email(body)

        if not failed_email or failed_email not in sent_emails or failed_email in existing_bounces:
            continue

        bounce_type = detect_bounce_type(body)
        append_bounce(failed_email, bounce_type)
        existing_bounces.add(failed_email)
        new_bounces += 1
        logger.info(f"Bounce detected: {failed_email} ({bounce_type})")

    return new_bounces

def main():
    if not mailer.should_run(email_config.RUN_BOUNCE_CHECK_AUTO):
        return

    since_date = (datetime.utcnow() - timedelta(days=DAYS_BACK)).strftime("%d-%b-%Y")
    logger.info(f"Checking bounces since {since_date}")

    try:
        sent_emails = load_sent_emails()
        existing_bounces = load_existing_bounces()

        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)

        folders_to_scan = ['[Gmail]/All Mail', '[Gmail]/Spam']
        total_new_bounces = 0

        for folder in folders_to_scan:
            try:
                total_new_bounces += process_folder(mail, folder, since_date, sent_emails, existing_bounces)
            except Exception as e:
                logger.error(f"Error scanning {folder}: {e}")

        if total_new_bounces == 0:
            logger.info("No new bounces found.")
        else:
            logger.info(f"Finished! Total new bounces detected: {total_new_bounces}")

        mail.logout()
    except Exception as e:
        logger.error(f"Bounce check failed: {e}")

if __name__ == "__main__":
    main()
