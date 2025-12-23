import smtplib
import logging
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
import email_config

# --- Logging Setup ---
LOG_FILE = "outreach.log"

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("mailer")

logger = setup_logging()

def should_run(auto_flag):
    """
    Determines if the script should run based on the automation flag
    and the execution environment.
    """
    event_name = os.environ.get("GITHUB_EVENT_NAME")
    
    # If not running in GitHub Actions, it's a local/manual run
    if not event_name:
        return True
        
    # If running as a scheduled action but auto is disabled, skip
    if event_name == "schedule" and not auto_flag:
        logger.info(f"Skipping scheduled run because automation is disabled in config.")
        return False
        
    # Manual workflow_dispatch or other events are allowed
    return True

def send_smtp_email(to_email, subject, body, attachment_path=None, dry_run=False):
    """
    Common function to send an email via SMTP.
    Supports attachments and dry-run mode.
    """
    if dry_run:
        logger.info(f"[DRY-RUN] Would send email to: {to_email}")
        logger.info(f"[DRY-RUN] Subject: {subject}")
        # logger.info(f"[DRY-RUN] Body: {body}") # Optional: noise reduction
        return True

    try:
        msg = MIMEMultipart()
        msg["From"] = email_config.EMAIL_ADDRESS
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        if attachment_path and os.path.exists(attachment_path):
            with open(attachment_path, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header("Content-Disposition", "attachment", filename=os.path.basename(attachment_path))
                msg.attach(attach)

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email_config.EMAIL_ADDRESS, email_config.EMAIL_PASSWORD)
        server.sendmail(email_config.EMAIL_ADDRESS, to_email, msg.as_string())
        server.quit()
        
        logger.info(f"Successfully sent email to: {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False
