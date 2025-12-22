#!/usr/bin/env python3
"""
Properly extract emails from PDF and append to CSV
"""
import re
import csv
import requests
from io import BytesIO
import PyPDF2

# Read existing emails
existing_emails = set()
with open('/app/emails.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        if row and len(row) >= 1:
            existing_emails.add(row[0].strip().lower())

print(f"Found {len(existing_emails)} existing emails")

# Download and process PDF
pdf_url = "https://customer-assets.emergentagent.com/job_19d122ed-37d6-4408-886c-e57377cd5e64/artifacts/t210jt1z_10%2C000-%20HR%20Emails%20For%20Candidates.pdf"
response = requests.get(pdf_url)
pdf_file = BytesIO(response.content)

# Extract text from PDF
pdf_reader = PyPDF2.PdfReader(pdf_file)
all_text = ""
for page in pdf_reader.pages:
    all_text += page.extract_text() + "\\n"

# Extract email addresses
email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
emails_found = re.findall(email_pattern, all_text)

print(f"Found {len(emails_found)} total emails in PDF")

# Process and deduplicate
new_entries = []
processed_emails = set()

for email in emails_found:
    email_lower = email.strip().lower()
    if email_lower in existing_emails or email_lower in processed_emails:
        continue
    
    processed_emails.add(email_lower)
    
    # Extract first name from email
    email_parts = email.split('@')[0]
    name_parts = email_parts.replace('.', ' ').replace('_', ' ').split()
    
    if name_parts:
        first_name = name_parts[0].capitalize()
    else:
        first_name = email_parts.capitalize()
    
    new_entries.append((email, first_name))

print(f"Found {len(new_entries)} new unique emails to add")

# Append to CSV properly
if new_entries:
    with open('/app/emails.csv', 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for email, name in new_entries:
            writer.writerow([email, name])
    
    print(f"Successfully appended {len(new_entries)} entries")
    
    # Verify
    total_lines = sum(1 for _ in open('/app/emails.csv'))
    print(f"Total lines in file (including header): {total_lines}")
else:
    print("No new entries to add")
