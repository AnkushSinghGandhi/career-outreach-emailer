import smtplib
import pandas as pd
import time
import os
import random
import yaml
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from tqdm import tqdm

# Import custom modules
from backup_manager import BackupManager
from logger_config import EmailLogger
from response_detector import ResponseDetector

# Parse command line arguments
parser = argparse.ArgumentParser(description='Enhanced Email Sender with Test Mode')
parser.add_argument('--test-mode', action='store_true', help='Run in test mode (uses test_emails.csv)')
parser.add_argument('--dry-run', action='store_true', help='Dry run - show what would be sent without sending')
args = parser.parse_args()

# Load configuration
with open("config.yaml", 'r') as f:
    config = yaml.safe_load(f)

# Apply test mode if enabled (CLI arg overrides config)
TEST_MODE = args.test_mode or config['test_mode']['enabled']
DRY_RUN = args.dry_run

# Initialize logger
logger = EmailLogger("send_email" + ("_test" if TEST_MODE else ""))

# Show mode banner
if TEST_MODE:
    logger.info("=" * 60)
    logger.info("🧪 TEST MODE ENABLED - Using test_emails.csv")
    logger.info("=" * 60)
elif DRY_RUN:
    logger.info("=" * 60)
    logger.info("🔍 DRY RUN MODE - No emails will be sent")
    logger.info("=" * 60)

# Initialize backup manager
backup_manager = BackupManager()

# Get credentials
EMAIL = os.environ.get("EMAIL_ADDRESS")
PASSWORD = os.environ.get("EMAIL_PASSWORD")

if not EMAIL or not PASSWORD:
    logger.error("EMAIL_ADDRESS and EMAIL_PASSWORD environment variables must be set")
    exit(1)

# Load configuration values
email_config = config['email']
test_config = config['test_mode']
retry_config = config['retry']
progress_config = config['progress']

# Use test mode settings if enabled
if TEST_MODE:
    files_config = {
        'contacts': test_config['test_contacts'],
        'sent_log': test_config['test_sent_log'],
        'followup_sent': test_config['test_followup_sent'],
        'replied': test_config['test_replied'],
        'resume': config['files']['resume']
    }
    LIMIT = test_config['limit']
    MIN_DELAY = test_config['min_delay']
    MAX_DELAY = test_config['max_delay']
else:
    files_config = config['files']
    LIMIT = email_config['limit']
    MIN_DELAY = email_config['min_delay']
    MAX_DELAY = email_config['max_delay']

# Create backup before starting
if backup_manager.backup_config['backup_before_run']:
    logger.info("Creating backup before starting...")
    backup_folder, backed_files = backup_manager.create_backup()
    if backup_folder:
        logger.success(f"Backup created: {backup_folder}")

# Check for responses (if enabled)
if config['response_detection']['enabled']:
    logger.info("Checking for email responses...")
    try:
        detector = ResponseDetector()
        new_replies = detector.check_responses()
        if new_replies:
            logger.success(f"Found {len(new_replies)} new responses!")
            for reply in new_replies:
                logger.info(f"  Reply from: {reply['email']}")
        else:
            logger.info("No new responses found.")
    except Exception as e:
        logger.warning(f"Could not check responses: {e}")

# Load email data
logger.info("Loading contact list...")
emails_df = pd.read_csv(files_config['contacts'])

if os.path.exists(files_config['sent_log']):
    sent_df = pd.read_csv(files_config['sent_log'])
    sent_emails = set(sent_df["email"].tolist())
else:
    sent_emails = set()
    pd.DataFrame(columns=["email"]).to_csv(files_config['sent_log'], index=False)

pending_df = emails_df[~emails_df["email"].isin(sent_emails)]

logger.info(f"Total contacts: {len(emails_df)}")
logger.info(f"Already sent: {len(sent_emails)}")
logger.info(f"Pending: {len(pending_df)}")
logger.info(f"Will send: {min(len(pending_df), LIMIT)} emails today")

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

ATTACHMENT_PATH = files_config['resume']


def generate_email_body(first_name):
    opening = random.choice(OPENINGS)
    signature = random.choice(SIGNATURES)

    body = f"""
Hi {first_name},

{opening}

I'm reaching out to explore opportunities for Python Backend roles within your organization or network. 
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


def send_email_with_retry(to_email, first_name):
    """Send email with retry mechanism"""
    max_attempts = retry_config['max_attempts'] if retry_config['enabled'] else 1
    
    for attempt in range(1, max_attempts + 1):
        try:
            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = to_email
            msg["Subject"] = random.choice(SUBJECTS)

            body_text = generate_email_body(first_name)
            msg.attach(MIMEText(body_text, "plain"))

            # Attach resume
            with open(ATTACHMENT_PATH, "rb") as f:
                attach = MIMEApplication(f.read(), _subtype="pdf")
                attach.add_header("Content-Disposition", "attachment", filename="Resume.pdf")
                msg.attach(attach)

            # Send email
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.sendmail(EMAIL, to_email, msg.as_string())
            server.quit()
            
            return True, None
        
        except Exception as e:
            if attempt < max_attempts:
                # Calculate backoff delay
                backoff_delay = retry_config['initial_delay'] * (retry_config['backoff_multiplier'] ** (attempt - 1))
                logger.warning(f"Attempt {attempt} failed for {to_email}. Retrying in {backoff_delay}s...")
                time.sleep(backoff_delay)
            else:
                return False, str(e)
    
    return False, "Max retries exceeded"


# Main sending loop
count = 0
success_count = 0
failed_count = 0
failed_emails = []

# Prepare progress bar
emails_to_send = pending_df.head(LIMIT)
total_emails = len(emails_to_send)

if total_emails == 0:
    logger.info("No emails to send!")
    exit(0)

logger.info(f"\n{'='*60}")
logger.info(f"Starting email campaign - {total_emails} emails")
logger.info(f"{'='*60}\n")

# Create progress bar
pbar = None
if progress_config['enabled']:
    pbar = tqdm(
        total=total_emails,
        desc="Sending emails",
        unit="email",
        colour=progress_config['color'],
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
    )

for _, row in emails_to_send.iterrows():
    to_email = row["email"]
    first_name = row.get("first_name", "") or "there"

    # Send email with retry
    success, error = send_email_with_retry(to_email, first_name)
    
    if success:
        logger.success(f"Sent to: {to_email}")
        
        # Log to CSV
        with open(files_config['sent_log'], "a") as log:
            log.write(f"{to_email}\n")
        
        success_count += 1
    else:
        logger.failed(f"Failed to send to {to_email}: {error}")
        failed_count += 1
        failed_emails.append({'email': to_email, 'error': error})
    
    count += 1
    
    # Update progress bar
    if pbar:
        pbar.update(1)
    
    # Delay before next email (except for last one)
    if count < total_emails:
        delay = random.randint(MIN_DELAY, MAX_DELAY)
        logger.debug(f"Waiting {delay} seconds before next email...")
        
        if pbar:
            pbar.set_postfix({'delay': f'{delay}s'})
        
        time.sleep(delay)

# Close progress bar
if pbar:
    pbar.close()

# Final statistics
logger.info(f"\n{'='*60}")
logger.info(f"Campaign Complete!")
logger.info(f"{'='*60}")
logger.info(f"Total sent: {success_count}")
logger.info(f"Failed: {failed_count}")
logger.info(f"Success rate: {(success_count/total_emails*100):.1f}%")

if failed_emails:
    logger.warning(f"\nFailed emails:")
    for failed in failed_emails:
        logger.warning(f"  - {failed['email']}: {failed['error']}")

logger.info(f"\nLogs saved to: logs/send_email_{time.strftime('%Y%m%d')}.log")
