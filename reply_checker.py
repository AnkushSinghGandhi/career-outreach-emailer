import imaplib
import email
import os
import pandas as pd
import email_config
import mailer
from datetime import datetime, timedelta

# ---------------- CONFIG ----------------
IMAP_HOST = "imap.gmail.com"
EMAIL_USER = email_config.EMAIL_ADDRESS
EMAIL_PASS = email_config.EMAIL_PASSWORD

REPLIED_CSV = "replied.csv"
SENT_LOG_CSV = "sent_log.csv"

DAYS_BACK = email_config.CHECK_DAYS_BACK
# ----------------------------------------

logger = mailer.logger

def load_sent_emails():
    if not os.path.exists(SENT_LOG_CSV):
        return set()
    df = pd.read_csv(SENT_LOG_CSV)
    if df.empty:
        return set()
    return {str(e).strip().lower() for e in df["email"].tolist()}

def load_existing_replies():
    if not os.path.exists(REPLIED_CSV):
        return set()
    df = pd.read_csv(REPLIED_CSV)
    if df.empty:
        return set()
    return {str(e).strip().lower() for e in df["email"].tolist()}

def append_reply(email_addr):
    file_exists = os.path.exists(REPLIED_CSV)
    df = pd.DataFrame([[email_addr, datetime.utcnow().strftime("%Y-%m-%d")]], columns=["email", "detected_on"])
    df.to_csv(REPLIED_CSV, mode="a", header=not file_exists, index=False)

def check_for_replies():
    if not mailer.should_run(email_config.RUN_REPLY_CHECK_AUTO):
        return

    since_date = (datetime.utcnow() - timedelta(days=DAYS_BACK)).strftime("%d-%b-%Y")
    logger.info(f"Checking for replies since {since_date}...")

    sent_emails = load_sent_emails()
    existing_replies = load_existing_replies()

    if not sent_emails:
        logger.info("No sent emails found in log. Skipping reply check.")
        return

    try:
        mail = imaplib.IMAP4_SSL(IMAP_HOST)
        mail.login(EMAIL_USER, EMAIL_PASS)
        mail.select("INBOX")

        # Search for all messages from sent emails
        new_replies = 0
        
        # Optimization: Instead of searching for EACH email, we search for all messages since date
        # and then filter in Python, or we could construct a complex search query.
        # Given potential Gmail search limits, let's search for messages since_date.
        status, messages = mail.search(None, f'(SINCE "{since_date}")')
        
        if status != "OK":
            logger.error("Could not search INBOX")
            return

        for num in messages[0].split():
            _, data = mail.fetch(num, "(RFC822)")
            msg = email.message_from_bytes(data[0][1])
            
            from_addr = email.utils.parseaddr(msg.get("From"))[1].lower()
            
            if from_addr in sent_emails and from_addr not in existing_replies:
                # Basic check: Is it actually a reply? 
                # Usually has Re: or In-Reply-To header, but for simple outreach, 
                # ANY email from them is likely a reply.
                logger.info(f"New reply detected from: {from_addr}")
                append_reply(from_addr)
                existing_replies.add(from_addr)
                new_replies += 1

        mail.logout()
        logger.info(f"Reply check finished. Detected {new_replies} new replies.")

    except Exception as e:
        logger.error(f"Error checking replies: {e}")

if __name__ == "__main__":
    check_for_replies()
