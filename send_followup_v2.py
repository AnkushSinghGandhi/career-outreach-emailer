import smtplib
import pandas as pd
import time
import os
import random
import yaml
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from tqdm import tqdm

# Import custom modules
from backup_manager import BackupManager
from logger_config import EmailLogger
from response_detector import ResponseDetector

# Parse command line arguments
parser = argparse.ArgumentParser(description='Enhanced Follow-up Email Sender with Test Mode')
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
logger = EmailLogger("send_followup" + ("_test" if TEST_MODE else ""))

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
    FOLLOWUP_LIMIT = test_config['limit']
    MIN_DELAY = test_config['min_delay']
    MAX_DELAY = test_config['max_delay']
else:
    files_config = config['files']
    FOLLOWUP_LIMIT = email_config['followup_limit']
    MIN_DELAY = email_config['followup_min_delay']
    MAX_DELAY = email_config['followup_max_delay']

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

# Load data
logger.info("Loading email tracking data...")
emails_df = pd.read_csv(files_config['contacts'])
sent_df = pd.read_csv(files_config['sent_log'])
replied_df = pd.read_csv(files_config['replied']) if os.path.exists(files_config['replied']) else pd.DataFrame(columns=["email"])
followup_df = pd.read_csv(files_config['followup_sent']) if os.path.exists(files_config['followup_sent']) else pd.DataFrame(columns=["email"])

sent_emails = set(sent_df["email"].tolist())
replied_emails = set(replied_df["email"].tolist())
followed_emails = set(followup_df["email"].tolist())

# Calculate pending follow-ups
pending_followup = [email for email in sent_emails if email not in replied_emails and email not in followed_emails]

logger.info(f"Total sent: {len(sent_emails)}")
logger.info(f"Replied: {len(replied_emails)}")
logger.info(f"Already followed up: {len(followed_emails)}")
logger.info(f"Pending follow-ups: {len(pending_followup)}")
logger.info(f"Will send: {min(len(pending_followup), FOLLOWUP_LIMIT)} follow-ups today")

SUBJECT_OPTIONS = [
    "Following up on my previous email",
    "Quick follow-up on my application",
    "Checking in regarding my earlier message",
    "Just circling back on my application",
    "Wanted to follow up on my previous note",
]

OPENERS = [
    "Hope you're doing well.",
    "Hope your day is going great.",
    "I hope you're having a productive week.",
    "Hope everything is going smoothly on your side.",
    "I hope you're doing well and staying healthy.",
]

BODY_VARIANTS = [
    """
I wanted to quickly follow up on my earlier message regarding potential Python/Backend Developer opportunities.

I understand things can get busy, so I just wanted to check in and see if you had a chance to review my previous email. 
I'm still very interested in any backend roles involving Python, Django, Flask, REST APIs, or database work.

If you need any additional details from my side, I'd be happy to share them.
""",

    """
Just following up on my previous email about backend roles.  
I know schedules get packed, so I thought I'd circle back to see if you had a moment to review my application.

I remain excited about opportunities involving Python, API development, and scalable backend systems.
If there's anything more you need, feel free to let me know.
""",

    """
I'm checking in regarding my earlier note about Python backend opportunities.

I understand hiring timelines vary, so no rush — just wanted to ensure my previous email didn't get missed.  
I'm still very much interested and open to discussing how my experience in Python, Django, Flask, and databases aligns with your team's needs.
""",

    """
Reaching out again to follow up on my previous message.

I know you receive many emails, so I wanted to check in politely. I'm still actively exploring opportunities that involve backend engineering, API development, and Python-based systems.
If there's any update or next step you'd recommend, I'd appreciate hearing from you.
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


def send_email_with_retry(to_email, first_name):
    """Send follow-up email with retry mechanism"""
    max_attempts = retry_config['max_attempts'] if retry_config['enabled'] else 1
    
    for attempt in range(1, max_attempts + 1):
        try:
            subject, full_body = build_email(first_name)

            msg = MIMEMultipart()
            msg["From"] = EMAIL
            msg["To"] = to_email
            msg["Subject"] = subject
            msg.attach(MIMEText(full_body, "plain"))

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

# Limit to FOLLOWUP_LIMIT
emails_to_send = pending_followup[:FOLLOWUP_LIMIT]
total_emails = len(emails_to_send)

if total_emails == 0:
    logger.info("No follow-up emails to send!")
    exit(0)

logger.info(f"\n{'='*60}")
logger.info(f"Starting follow-up campaign - {total_emails} emails")
logger.info(f"{'='*60}\n")

# Create progress bar
pbar = None
if progress_config['enabled']:
    pbar = tqdm(
        total=total_emails,
        desc="Sending follow-ups",
        unit="email",
        colour=progress_config['color'],
        bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]'
    )

for email_addr in emails_to_send:
    # Get first name from original contacts
    row = emails_df[emails_df["email"] == email_addr]
    first_name = row["first_name"].iloc[0] if "first_name" in row.columns and len(row) > 0 else "there"

    # Send email with retry
    success, error = send_email_with_retry(email_addr, first_name)
    
    if success:
        logger.success(f"Follow-up sent to: {email_addr}")
        
        # Log to CSV
        pd.DataFrame([[email_addr]], columns=["email"]).to_csv(
            files_config['followup_sent'], 
            mode="a", 
            header=False, 
            index=False
        )
        
        success_count += 1
    else:
        logger.failed(f"Failed to send to {email_addr}: {error}")
        failed_count += 1
        failed_emails.append({'email': email_addr, 'error': error})
    
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
logger.info(f"Follow-up Campaign Complete!")
logger.info(f"{'='*60}")
logger.info(f"Total sent: {success_count}")
logger.info(f"Failed: {failed_count}")
logger.info(f"Success rate: {(success_count/total_emails*100):.1f}%")

if failed_emails:
    logger.warning(f"\nFailed emails:")
    for failed in failed_emails:
        logger.warning(f"  - {failed['email']}: {failed['error']}")

logger.info(f"\nLogs saved to: logs/send_followup_{time.strftime('%Y%m%d')}.log")
