#!/usr/bin/env python3
"""
Script to extract emails and names from PDF and append to emails.csv
"""
import re
import csv
from pathlib import Path

# Read the existing emails.csv to find the last line number
existing_emails = set()
last_line = 1

csv_path = Path('/app/emails.csv')
if csv_path.exists():
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)  # Skip header
        for row in reader:
            if row and len(row) >= 1:
                last_line += 1
                if len(row) >= 1:
                    existing_emails.add(row[0].strip().lower())

print(f"Found {len(existing_emails)} existing emails")
print(f"Last line number: {last_line}")

# Parse the extracted data from the PDF
# The data contains email,first_name pairs
extracted_text = """akanksha.puri@sourcefuse.com,Akanksha
alok.singh@recro.io,Alok
alok.kumar@vfislk.com,Alok
alwyn.barretto@infrasofttech.com,Alwyn
aman.khan@areteanstech.com,Aman
amandeep.k@antiersolutions.com,Amandeep
amar.sinha@nitorinfotech.com,Amar
ambrish.kanungo@beyondkey.com,Ambrish
amiit.avaasthi@altudo.co,Amiit"""

# In this case, let me download and process the PDF properly
print("\\nProcessing PDF to extract new entries...")

# Since the extraction returned garbled data, let's create a simple approach
# We'll write a script to download and process the PDF properly
import requests
from io import BytesIO

try:
    import PyPDF2
    print("PyPDF2 is available")
except ImportError:
    print("Installing PyPDF2...")
    import subprocess
    subprocess.run(['pip', 'install', 'PyPDF2'], check=True)
    import PyPDF2

# Download the PDF
pdf_url = "https://customer-assets.emergentagent.com/job_19d122ed-37d6-4408-886c-e57377cd5e64/artifacts/t210jt1z_10%2C000-%20HR%20Emails%20For%20Candidates.pdf"
response = requests.get(pdf_url)
pdf_file = BytesIO(response.content)

# Extract text from PDF
pdf_reader = PyPDF2.PdfReader(pdf_file)
all_text = ""
for page in pdf_reader.pages:
    all_text += page.extract_text()

# Extract email addresses and try to find associated names
email_pattern = r'([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})'
name_pattern = r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)'

emails_found = re.findall(email_pattern, all_text)
print(f"Found {len(emails_found)} emails in PDF")

# Try to extract name from email or find nearby text
new_entries = []
processed_emails = set()

for email in emails_found:
    email_lower = email.strip().lower()
    if email_lower in existing_emails or email_lower in processed_emails:
        continue
    
    processed_emails.add(email_lower)
    
    # Extract first name from email (before @ or first dot)
    email_parts = email.split('@')[0]
    name_parts = email_parts.replace('.', ' ').replace('_', ' ').split()
    
    if name_parts:
        first_name = name_parts[0].capitalize()
    else:
        first_name = email_parts.capitalize()
    
    new_entries.append((email, first_name))

print(f"\\nFound {len(new_entries)} new unique emails to add")

# Append to CSV
if new_entries:
    with open(csv_path, 'a', encoding='utf-8', newline='') as f:
        for email, name in new_entries:
            f.write(f"{email},{name}\\n")
    
    print(f"\\nSuccessfully appended {len(new_entries)} new entries to emails.csv")
    print(f"Total entries in file now: {last_line + len(new_entries)}")
else:
    print("\\nNo new entries to add - all emails already exist in the file")

