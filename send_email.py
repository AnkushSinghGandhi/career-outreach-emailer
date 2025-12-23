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
    parser = argparse.ArgumentParser(description="Send outreach emails.")
    parser.add_argument("--dry-run", action="store_true", help="Print emails instead of sending them.")
    return parser.parse_args()

def generate_email_body(first_name):
    opening = random.choice(email_config.INITIAL_OPENINGS)
    signature = random.choice(email_config.INITIAL_SIGNATURES)

    body = email_config.INITIAL_BODY_TEMPLATE.format(
        first_name=first_name,
        opening=opening,
        signature=signature,
        links=email_config.LINKS
    )
    return body

def main():
    args = parse_args()
    
    if not mailer.should_run(email_config.RUN_OUTREACH_AUTO):
        return

    if args.dry_run:
        logger.info("Running in DRY-RUN mode. No emails will be sent.")

    emails_df = pd.read_csv("emails.csv")

    if os.path.exists("sent_log.csv"):
        sent_df = pd.read_csv("sent_log.csv")
        sent_emails = set(sent_df["email"].tolist())
    else:
        sent_emails = set()
        pd.DataFrame(columns=["email"]).to_csv("sent_log.csv", index=False)

    pending_df = emails_df[~emails_df["email"].isin(sent_emails)]

    limit = email_config.INITIAL_LIMIT
    count = 0

    for _, row in pending_df.iterrows():
        if count >= limit:
            logger.info("Daily limit reached.")
            break

        to_email = row["email"]
        first_name = row.get("first_name", "") or ""

        subject = random.choice(email_config.INITIAL_SUBJECTS)
        body = generate_email_body(first_name)

        success = mailer.send_smtp_email(
            to_email=to_email,
            subject=subject,
            body=body,
            attachment_path=email_config.ATTACHMENT_PATH,
            dry_run=args.dry_run
        )

        if success:
            if not args.dry_run:
                with open("sent_log.csv", "a") as log:
                    log.write(f"{to_email}\n")
            
            count += 1
            delay = random.randint(email_config.INITIAL_MIN_DELAY, email_config.INITIAL_MAX_DELAY)
            logger.info(f"Sleeping for {delay} seconds...")
            time.sleep(delay)
        else:
            time.sleep(5)

if __name__ == "__main__":
    main()
