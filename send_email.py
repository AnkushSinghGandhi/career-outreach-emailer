import smtplib
import pandas as pd
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os

EMAIL = os.environ['EMAIL_ADDRESS']
PASSWORD = os.environ['EMAIL_PASSWORD']

df = pd.read_csv("emails.csv")

SUBJECT = "Application for Python/Backend Developer Position"

BODY = """
Hi {first_name},
I noticed that you are currently hiring for Python roles, and I wanted to reach out directly. With 2+ years of experience as  Python Backend Developer, I am confident in my ability to contribute effectively to your team and believe my skills in building scalable systems using Flask, Django, REST APIs, and SQL/NoSQL databases (MySQL, MongoDB, Redis) align well with the requirements of the role.

What excites me most is the chance to bring this mix of backend expertise, cloud deployment, and real-time data experience to opportunities your team is hiring for. I’d love to connect and share my resume for your consideration.

Thank you for considering my application. I have attached my resume for your review. I would welcome the opportunity to discuss how my background, skills, and passion for building scalable backend systems make me a strong candidate for this position.

I look forward to hearing from you soon.

Best regards,
Ankush Singh Gandhi
 +91-95296-39652
https://warriorwhocodes.com
https://www.linkedin.com/in/ankushsinghgandhi
"""

ATTACHMENT_PATH = "resume.pdf"   # upload this file also

def send_email(to_email, first_name):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = to_email
    msg['Subject'] = SUBJECT

    msg.attach(MIMEText(BODY.format(name=first_name), "plain"))

    with open(ATTACHMENT_PATH, "rb") as f:
        attach = MIMEApplication(f.read(), _subtype="pdf")
        attach.add_header('Content-Disposition', 'attachment', filename="Resume.pdf")
        msg.attach(attach)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL, PASSWORD)
    server.sendmail(EMAIL, to_email, msg.as_string())
    server.quit()


count = 0
LIMIT = 100   # send 100 emails per day
DELAY = 20    # delay between emails (seconds)

for _, row in df.iterrows():
    if count >= LIMIT:
        break
    to_email = row['email']
    first_name = row.get('first_name', '')
    try:
        send_email(to_email, first_name)
        print("Sent:", to_email)
        count += 1
        time.sleep(DELAY)
    except Exception as e:
        print("Failed:", to_email, e)
        time.sleep(5)
