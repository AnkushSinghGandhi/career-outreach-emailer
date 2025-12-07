import imaplib
import email
from email.header import decode_header
import os
import pandas as pd
from datetime import datetime, timedelta
import yaml

class ResponseDetector:
    """Automatically detect email responses using Gmail IMAP"""
    
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.response_config = self.config['response_detection']
        self.files_config = self.config['files']
        
        self.email_address = os.environ.get("EMAIL_ADDRESS")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        
        if not self.email_address or not self.email_password:
            raise ValueError("EMAIL_ADDRESS and EMAIL_PASSWORD must be set")
    
    def connect_imap(self):
        """Connect to Gmail IMAP server"""
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email_address, self.email_password)
            return mail
        except Exception as e:
            raise ConnectionError(f"Failed to connect to IMAP: {e}")
    
    def get_sender_email(self, from_header):
        """Extract email address from From header"""
        # Handle formats like: "John Doe <john@example.com>" or "john@example.com"
        if '<' in from_header and '>' in from_header:
            return from_header.split('<')[1].split('>')[0].strip().lower()
        return from_header.strip().lower()
    
    def check_responses(self, days=None):
        """Check for email responses in the last N days"""
        if not self.response_config['enabled']:
            return []
        
        if days is None:
            days = self.response_config['check_days']
        
        # Load sent emails
        sent_df = pd.read_csv(self.files_config['sent_log'])
        sent_emails = set(sent_df['email'].str.lower().tolist())
        
        # Load already replied emails
        replied_file = self.files_config['replied']
        if os.path.exists(replied_file):
            replied_df = pd.read_csv(replied_file)
            already_replied = set(replied_df['email'].str.lower().tolist())
        else:
            already_replied = set()
            # Create the file
            pd.DataFrame(columns=['email', 'reply_date']).to_csv(replied_file, index=False)
        
        # Connect to IMAP
        try:
            mail = self.connect_imap()
        except Exception as e:
            print(f"Could not connect to IMAP: {e}")
            return []
        
        new_replies = []
        
        try:
            # Select inbox
            mail.select('INBOX')
            
            # Calculate date range
            since_date = (datetime.now() - timedelta(days=days)).strftime("%d-%b-%Y")
            
            # Search for emails since date
            status, messages = mail.search(None, f'(SINCE {since_date})')
            
            if status != 'OK':
                return new_replies
            
            email_ids = messages[0].split()
            
            # Process emails
            for email_id in email_ids:
                try:
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                    
                    # Parse email
                    msg = email.message_from_bytes(msg_data[0][1])
                    
                    # Get sender
                    from_header = msg.get('From', '')
                    sender_email = self.get_sender_email(from_header)
                    
                    # Check if this is from someone we emailed
                    if sender_email in sent_emails and sender_email not in already_replied:
                        # Get date
                        date_str = msg.get('Date', '')
                        
                        new_replies.append({
                            'email': sender_email,
                            'reply_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'subject': msg.get('Subject', ''),
                            'date_received': date_str
                        })
                        
                        already_replied.add(sender_email)
                
                except Exception as e:
                    # Skip problematic emails
                    continue
            
            # Update replied.csv if auto-update is enabled
            if new_replies and self.response_config['auto_update_replied']:
                self._update_replied_csv(new_replies)
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            print(f"Error checking responses: {e}")
        
        return new_replies
    
    def _update_replied_csv(self, new_replies):
        """Update replied.csv with new responses"""
        replied_file = self.files_config['replied']
        
        # Load existing data
        if os.path.exists(replied_file):
            df = pd.read_csv(replied_file)
        else:
            df = pd.DataFrame(columns=['email', 'reply_date'])
        
        # Add new replies
        for reply in new_replies:
            new_row = pd.DataFrame([{
                'email': reply['email'],
                'reply_date': reply['reply_date']
            }])
            df = pd.concat([df, new_row], ignore_index=True)
        
        # Remove duplicates
        df = df.drop_duplicates(subset=['email'], keep='first')
        
        # Save
        df.to_csv(replied_file, index=False)
    
    def get_response_stats(self):
        """Get statistics about responses"""
        sent_file = self.files_config['sent_log']
        replied_file = self.files_config['replied']
        
        if not os.path.exists(sent_file):
            return None
        
        sent_count = len(pd.read_csv(sent_file))
        
        replied_count = 0
        if os.path.exists(replied_file):
            replied_count = len(pd.read_csv(replied_file))
        
        response_rate = (replied_count / sent_count * 100) if sent_count > 0 else 0
        
        return {
            'total_sent': sent_count,
            'total_replied': replied_count,
            'response_rate': round(response_rate, 2),
            'no_response': sent_count - replied_count
        }

if __name__ == "__main__":
    # Test response detector
    try:
        detector = ResponseDetector()
        print("Checking for responses...")
        replies = detector.check_responses()
        
        if replies:
            print(f"\nFound {len(replies)} new responses:")
            for reply in replies:
                print(f"  - {reply['email']} replied on {reply['reply_date']}")
        else:
            print("No new responses found.")
        
        # Show stats
        stats = detector.get_response_stats()
        if stats:
            print(f"\nResponse Statistics:")
            print(f"  Total Sent: {stats['total_sent']}")
            print(f"  Total Replied: {stats['total_replied']}")
            print(f"  Response Rate: {stats['response_rate']}%")
    
    except Exception as e:
        print(f"Error: {e}")
