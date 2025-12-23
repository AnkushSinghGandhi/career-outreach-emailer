import pandas as pd
import time
import os
import random
import argparse
import email_config
import mailer

# Setup logging
logger = mailer.logger

def parse_args():
    parser = argparse.ArgumentParser(description="Send follow-up emails.")
    parser.add_argument("--dry-run", action="store_true", help="Print emails instead of sending them.")
    return parser.parse_args()

def build_email(first_name):
    subject = random.choice(email_config.FOLLOWUP_SUBJECTS)
    opener = random.choice(email_config.FOLLOWUP_OPENERS)
    body = random.choice(email_config.FOLLOWUP_BODY_VARIANTS)
    signature = random.choice(email_config.FOLLOWUP_SIGNATURES)

    final_body = email_config.FOLLOWUP_BODY_TEMPLATE.format(
        first_name=first_name,
        opener=opener,
        body=body,
        signature=signature
    )
    return subject, final_body

def main():
    args = parse_args()
    
    if not mailer.should_run(email_config.RUN_FOLLOWUP_AUTO):
        return

    if args.dry_run:
        logger.info("Running in DRY-RUN mode. No follow-ups will be sent.")

    emails_df = pd.read_csv("emails.csv")
    sent_df = pd.read_csv("sent_log.csv")
    
    replied_df = pd.read_csv("replied.csv") if os.path.exists("replied.csv") else pd.DataFrame(columns=["email"])
    followup_df = pd.read_csv("followup_sent.csv") if os.path.exists("followup_sent.csv") else pd.DataFrame(columns=["email"])

    sent_emails = set(sent_df["email"].tolist())
    replied_emails = set(replied_df["email"].tolist())
    followed_emails = set(followup_df["email"].tolist())

    pending_followup = [email for email in sent_emails if email not in replied_emails and email not in followed_emails]

    logger.info(f"Follow-up emails to send today: {len(pending_followup)}")

    limit = email_config.FOLLOWUP_LIMIT
    count = 0

    for email in pending_followup:
        if count >= limit:
            logger.info("Follow-up limit reached.")
            break

        row = emails_df[emails_df["email"] == email]
        first_name = row["first_name"].iloc[0] if "first_name" in row and len(row) > 0 else ""

        subject, full_body = build_email(first_name)

        success = mailer.send_smtp_email(
            to_email=email,
            subject=subject,
            body=full_body,
            dry_run=args.dry_run
        )

        if success:
            if not args.dry_run:
                pd.DataFrame([[email]], columns=["email"]).to_csv("followup_sent.csv", mode="a", header=False, index=False)
            
            count += 1
            delay = random.randint(email_config.FOLLOWUP_MIN_DELAY, email_config.FOLLOWUP_MAX_DELAY)
            logger.info(f"Sleeping for {delay} seconds...")
            time.sleep(delay)
        else:
            time.sleep(5)

if __name__ == "__main__":
    main()
