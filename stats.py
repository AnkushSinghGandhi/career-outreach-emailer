import pandas as pd
import os

def get_csv_count(filename):
    if not os.path.exists(filename):
        return 0
    try:
        df = pd.read_csv(filename)
        return len(df)
    except Exception:
        return 0

def show_stats():
    total_contacts = get_csv_count("emails.csv")
    sent_emails = get_csv_count("sent_log.csv")
    followups_sent = get_csv_count("followup_sent.csv")
    replies = get_csv_count("replied.csv")
    bounces = get_csv_count("bounced_emails.csv")

    pending = total_contacts - sent_emails

    print("\n" + "="*30)
    print("      CAMPAIGN STATISTICS")
    print("="*30)
    print(f"Total Contacts:    {total_contacts}")
    print(f"Emails Sent:       {sent_emails}")
    print(f"Pending Outreach:  {pending}")
    print(f"Follow-ups Sent:   {followups_sent}")
    print("-" * 30)
    print(f"Replies Detected:  {replies}")
    print(f"Bounces Detected:  {bounces}")
    
    if sent_emails > 0:
        reply_rate = (replies / sent_emails) * 100
        bounce_rate = (bounces / sent_emails) * 100
        print("-" * 30)
        print(f"Reply Rate:        {reply_rate:.2f}%")
        print(f"Bounce Rate:       {bounce_rate:.2f}%")
    print("="*30 + "\n")

if __name__ == "__main__":
    show_stats()
