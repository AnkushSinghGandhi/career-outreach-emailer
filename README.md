# 📧 Email Automation Tool for Job Applications

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Gmail](https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)

**Automate your job application emails with intelligence and personalization** 🚀

*Send personalized emails, track responses, and follow up automatically - all while staying under the radar!*

[Features](#-features) • [Quick Start](#-quick-start) • [Installation](#-installation) • [Usage](#-usage) • [GitHub Actions](#-github-actions-automation)

</div>

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🚀 Quick Start](#-quick-start)
- [📦 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [📊 CSV File Setup](#-csv-file-setup)
- [💻 Usage](#-usage)
- [🤖 GitHub Actions Automation](#-github-actions-automation)
- [🔧 Advanced Configuration](#-advanced-configuration)
- [📈 Best Practices](#-best-practices)
- [🛡️ Safety & Ethics](#️-safety--ethics)
- [🐛 Troubleshooting](#-troubleshooting)
- [🏗️ Architecture](#️-architecture)
- [🤝 Contributing](#-contributing)
- [📄 License](#-license)
- [⚠️ Disclaimer](#️-disclaimer)

---

## ✨ Features

### 🎯 Core Features

| Feature | Description |
|---------|-------------|
| 📨 **Automated Email Sending** | Send personalized job application emails with resume attachment |
| 🔄 **Smart Follow-ups** | Automatically send follow-up emails to non-responders |
| 🎲 **Anti-Spam Randomization** | Randomize subjects, openings, and signatures to appear natural |
| ⏱️ **Rate Limiting** | Built-in delays (50-120s) between emails to avoid spam detection |
| 📊 **CSV Tracking** | Track sent emails and follow-ups automatically |
| 👤 **Personalization** | Use first names for personalized greetings |
| 📎 **Resume Attachment** | Automatically attach your resume to each email |
| 🔐 **Secure Credentials** | Use environment variables for email credentials |

### 🤖 Automation Features

- **GitHub Actions Integration** - Run automatically on schedule or manually
- **Daily Email Sending** - Automated cron job (3:30 AM UTC daily)
- **Manual Triggers** - Send emails or follow-ups on-demand
- **Auto-commit Logs** - Automatically update tracking CSVs to repository

### 💡 Smart Features

- ✅ Duplicate prevention - Never send to the same person twice
- ✅ Response tracking - Skip follow-ups if they replied
- ✅ Configurable limits - 125 initial emails + 40 follow-ups per day
- ✅ Error handling - Continue on failures with detailed logging
- ✅ Random delays - Variable timing to mimic human behavior

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/email-automation.git
cd email-automation

# Install dependencies
pip install pandas

# Set up environment variables
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"

# Prepare your contact list
# Edit emails.csv with your contacts

# Send emails
python send_email.py

# Send follow-ups (after a few days)
python send_followup.py
```

---

## 📦 Installation

### Prerequisites

- **Python 3.10+** - [Download here](https://www.python.org/downloads/)
- **Gmail Account** - With 2FA enabled
- **Gmail App Password** - [How to create](#creating-gmail-app-password)
- **Git** (optional) - For version control

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/email-automation.git
cd email-automation
```

### Step 2: Install Python Dependencies

```bash
pip install pandas
```

**Dependencies:**
- `pandas` - For CSV operations
- `smtplib` - Built-in Python library for SMTP
- `email` - Built-in Python library for email composition

### Step 3: Create Gmail App Password

Since Gmail requires app-specific passwords for third-party applications:

1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** (if not already enabled)
3. Search for **App passwords**
4. Select app: **Mail**
5. Select device: **Other (Custom name)** - Enter "Email Automation"
6. Copy the generated 16-character password

**⚠️ Important:** Keep this password secure and never commit it to version control!

---

## ⚙️ Configuration

### Environment Variables

Set up your email credentials as environment variables:

#### On Linux/Mac:

```bash
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-16-char-app-password"
```

**To make it permanent**, add to `~/.bashrc` or `~/.zshrc`:

```bash
echo 'export EMAIL_ADDRESS="your-email@gmail.com"' >> ~/.bashrc
echo 'export EMAIL_PASSWORD="your-app-password"' >> ~/.bashrc
source ~/.bashrc
```

#### On Windows (PowerShell):

```powershell
$env:EMAIL_ADDRESS="your-email@gmail.com"
$env:EMAIL_PASSWORD="your-16-char-app-password"
```

**To make it permanent**, add to System Environment Variables:
1. Search for "Environment Variables" in Windows
2. Click "New" under User Variables
3. Add `EMAIL_ADDRESS` and `EMAIL_PASSWORD`

#### Using .env File (Alternative):

Create a `.env` file in the project root:

```bash
EMAIL_ADDRESS=your-email@gmail.com
EMAIL_PASSWORD=your-16-char-app-password
```

Then modify scripts to load from `.env`:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📊 CSV File Setup

### 1. emails.csv (Contact List)

This file contains all your target recipients:

```csv
email,first_name
john.doe@company.com,John
jane.smith@startup.io,Jane
recruiter@techcorp.com,Sarah
```

**Format:**
- **email** - Valid email address
- **first_name** - First name for personalization (optional)

### 2. sent_log.csv (Tracking Sent Emails)

Auto-generated. Tracks emails that have been sent:

```csv
email
john.doe@company.com
jane.smith@startup.io
```

### 3. followup_sent.csv (Tracking Follow-ups)

Auto-generated. Tracks follow-up emails:

```csv
email
john.doe@company.com
```

### 4. replied.csv (Optional - Response Tracking)

Create this manually to track who replied:

```csv
email
jane.smith@startup.io
```

**💡 Tip:** Anyone in `replied.csv` will be skipped from follow-ups!

---

## 💻 Usage

### Sending Initial Emails

Run the main email sender script:

```bash
python send_email.py
```

**What happens:**
1. ✅ Reads contacts from `emails.csv`
2. ✅ Skips emails already in `sent_log.csv`
3. ✅ Sends up to **125 emails** per run
4. ✅ Attaches `resume.pdf` to each email
5. ✅ Waits 50-120 seconds between emails
6. ✅ Logs sent emails to `sent_log.csv`

**Example Output:**

```
Sent: john.doe@company.com
Sleeping for 87 seconds...
Sent: jane.smith@startup.io
Sleeping for 103 seconds...
Failed: invalid@email.com - SMTP Error
```

### Sending Follow-up Emails

After 3-5 days, send follow-ups to non-responders:

```bash
python send_followup.py
```

**What happens:**
1. ✅ Finds emails in `sent_log.csv` but not in `replied.csv` or `followup_sent.csv`
2. ✅ Sends up to **40 follow-ups** per run
3. ✅ Uses different subject lines and body variations
4. ✅ Waits 40-60 seconds between emails
5. ✅ Logs to `followup_sent.csv`

**Example Output:**

```
Follow-up emails to send today: 87
Follow-up sent: john.doe@company.com
Sleeping for 52 seconds...
Follow-up sent: recruiter@techcorp.com
Sleeping for 45 seconds...
Follow-up limit reached.
```

---

## 🤖 GitHub Actions Automation

This project includes **two automated workflows** that run on GitHub's servers:

### 🔄 Workflow 1: Daily Email Sender

**File:** `.github/workflows/send-emails.yml`

**Trigger:**
- 🕒 **Scheduled:** Every day at 3:30 AM UTC (automatically)
- 🖱️ **Manual:** Click "Run workflow" in GitHub Actions tab

**What it does:**
1. ✅ Checks out your repository
2. ✅ Sets up Python 3.10
3. ✅ Installs dependencies
4. ✅ Runs `send_email.py` with your secrets
5. ✅ Commits updated `sent_log.csv` back to repo

**Schedule:** `cron: "30 3 * * *"`
- Runs at 3:30 AM UTC daily
- Adjust timezone as needed (9:00 AM IST = 3:30 AM UTC)

### 📬 Workflow 2: Follow-up Sender

**File:** `.github/workflows/send_followups.yml`

**Trigger:**
- 🖱️ **Manual only:** You control when to send follow-ups

**What it does:**
1. ✅ Checks out your repository
2. ✅ Sets up Python 3.10
3. ✅ Installs dependencies
4. ✅ Runs `send_followup.py` with your secrets
5. ✅ Commits updated `followup_sent.csv` back to repo

### 🔐 Setting Up GitHub Secrets

To enable GitHub Actions, add your credentials as secrets:

1. Go to your repository on GitHub
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add two secrets:

| Name | Value |
|------|-------|
| `EMAIL_ADDRESS` | your-email@gmail.com |
| `EMAIL_PASSWORD` | your-16-char-app-password |

### 🎮 Running Workflows Manually

1. Go to **Actions** tab in your GitHub repository
2. Select the workflow you want to run:
   - **Send Daily Emails** - For initial outreach
   - **Send Follow-up Emails** - For follow-ups
3. Click **Run workflow** button
4. Select branch (usually `main`)
5. Click **Run workflow** again

### 📊 Monitoring Workflow Runs

- View logs in the **Actions** tab
- Check commit history for automated updates to CSVs
- Email yourself a summary (optional enhancement)

### 🎯 Workflow Schedule Customization

Want to change the schedule? Edit `.github/workflows/send-emails.yml`:

```yaml
schedule:
  - cron: "30 3 * * *"  # 3:30 AM UTC daily
```

**Common schedules:**

| Time | Cron Expression | Description |
|------|----------------|-------------|
| 9:00 AM IST | `"30 3 * * *"` | Current setting |
| 8:00 AM EST | `"0 13 * * *"` | US East Coast morning |
| 10:00 AM CET | `"0 9 * * *"` | Europe morning |
| Every 2 days | `"30 3 */2 * *"` | Every other day |
| Weekdays only | `"30 3 * * 1-5"` | Monday-Friday |

**🔍 Cron Helper:** Use [crontab.guru](https://crontab.guru/) to create custom schedules

### ⚡ GitHub Actions Benefits

✅ **No Local Machine Required** - Runs on GitHub's servers
✅ **Fully Automated** - Set it and forget it
✅ **Free** - 2,000 minutes/month on free tier
✅ **Reliable** - Never miss a day
✅ **Version Controlled** - All logs tracked in Git
✅ **Scalable** - Can handle large contact lists

---

## 🔧 Advanced Configuration

### Customizing Email Limits

Edit `send_email.py`:

```python
LIMIT = 125  # Change to your desired daily limit
```

Edit `send_followup.py`:

```python
FOLLOWUP_LIMIT = 40  # Change follow-up limit
```

### Adjusting Delays

Edit timing between emails:

```python
# In send_email.py
MIN_DELAY = 50   # Minimum seconds between emails
MAX_DELAY = 120  # Maximum seconds between emails

# In send_followup.py
MIN_DELAY = 40   # Faster for follow-ups
MAX_DELAY = 60
```

**⚠️ Warning:** Shorter delays increase spam detection risk!

### Customizing Email Content

#### Adding New Subject Lines

Edit `send_email.py`:

```python
SUBJECTS = [
    "Application for Python/Backend Developer Role",
    "Your Custom Subject Here",  # Add your own
    # ... more subjects
]
```

#### Adding New Email Openings

```python
OPENINGS = [
    "I hope you're doing well.",
    "Your custom opening here",  # Add your own
    # ... more openings
]
```

#### Modifying Email Body

Edit the `generate_email_body()` function:

```python
def generate_email_body(first_name):
    opening = random.choice(OPENINGS)
    signature = random.choice(SIGNATURES)
    
    body = f"""
Hi {first_name},

{opening}

[YOUR CUSTOM MESSAGE HERE]

{signature}
{LINKS}
"""
    return body
```

### Adding Your Details

Update personal information:

```python
# In send_email.py
SIGNATURES = [
    "Best regards,\nYour Name\n+91-XXXXXXXXXX",
    "Warm regards,\nYour Name\n+91-XXXXXXXXXX",
    # ... add more variations
]

LINKS = "\nYourWebsite.com\nhttps://linkedin.com/in/yourprofile"
```

### Changing Resume File

Replace `resume.pdf` with your resume, or change the path:

```python
ATTACHMENT_PATH = "path/to/your/resume.pdf"
```

---

## 📈 Best Practices

### 📝 Email Strategy

| Best Practice | Why It Matters |
|--------------|----------------|
| 🎯 **Target Specific Roles** | Higher response rates from relevant contacts |
| 📅 **Wait 3-5 Days for Follow-ups** | Gives recipients time to respond |
| 📊 **Track Responses** | Update `replied.csv` to avoid annoying responders |
| ✉️ **Quality Over Quantity** | 50 targeted emails > 500 spray-and-pray |
| 🕐 **Send During Business Hours** | Use GitHub Actions schedule wisely |

### 🚀 Optimization Tips

1. **Segment Your List**
   ```csv
   # Create role-specific CSVs
   emails_backend.csv
   emails_fullstack.csv
   emails_senior.csv
   ```

2. **A/B Test Subject Lines**
   - Track which subjects get replies
   - Remove underperforming variants

3. **Personalize When Possible**
   - Research companies before adding to list
   - Add company-specific notes if needed

4. **Monitor Spam Scores**
   - Use [Mail Tester](https://www.mail-tester.com/)
   - Avoid spam trigger words
   - Keep formatting simple

5. **Maintain Email Reputation**
   - Don't exceed daily limits
   - Remove bounced emails
   - Honor unsubscribe requests

### 🔐 Security Best Practices

✅ **DO:**
- Use app-specific passwords
- Store credentials in environment variables
- Enable 2FA on your Gmail account
- Regularly rotate passwords
- Keep `.env` in `.gitignore`

❌ **DON'T:**
- Commit credentials to Git
- Share app passwords
- Use your main Gmail password
- Store passwords in code
- Exceed Gmail's daily sending limits

---

## 🛡️ Safety & Ethics

### ⚠️ Important Guidelines

#### 🟢 Ethical Use

✅ **Allowed:**
- Sending genuine job applications
- Following up on your applications
- Contacting publicly listed recruiters
- Personalizing each email
- Respecting opt-out requests

#### 🔴 Prohibited

❌ **NOT Allowed:**
- Sending unsolicited marketing
- Harvesting emails without consent
- Ignoring unsubscribe requests
- Sending to scraped email lists
- Impersonating others
- Spamming indiscriminately

### 📜 Legal Considerations

- **CAN-SPAM Act (USA):** Include physical address and opt-out method
- **GDPR (EU):** Ensure lawful basis for processing contact info
- **CASL (Canada):** Obtain consent before sending commercial emails

**💡 Recommendation:** Add an unsubscribe line to your email template:

```python
body = f"""
Hi {first_name},

[Your message]

{signature}

P.S. If you'd prefer not to receive future messages, please reply with "Unsubscribe"
"""
```

### 🎯 Staying Under the Radar

| Tip | Description |
|-----|-------------|
| 🐢 **Slow and Steady** | Respect delays - don't rush |
| 🎲 **Randomize Everything** | Subjects, timings, wording |
| 📊 **Monitor Bounce Rates** | Remove invalid emails quickly |
| 🔄 **Rotate Subject Lines** | Add new variations regularly |
| 📧 **Warm Up New Accounts** | Start with 20-30 emails/day for new accounts |

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### 🔴 Authentication Failed

**Error:** `smtplib.SMTPAuthenticationError: (535, '5.7.8 Username and Password not accepted')`

**Solutions:**
1. ✅ Verify you're using **App Password**, not regular password
2. ✅ Check environment variables are set correctly:
   ```bash
   echo $EMAIL_ADDRESS
   echo $EMAIL_PASSWORD
   ```
3. ✅ Ensure 2FA is enabled on Gmail
4. ✅ Regenerate App Password if needed

#### 🔴 SMTP Connection Error

**Error:** `smtplib.SMTPServerDisconnected: Connection unexpectedly closed`

**Solutions:**
1. ✅ Check internet connection
2. ✅ Verify Gmail SMTP settings:
   - Server: `smtp.gmail.com`
   - Port: `587`
3. ✅ Disable VPN temporarily
4. ✅ Check firewall settings

#### 🔴 Daily Limit Exceeded

**Error:** `smtplib.SMTPSenderRefused: (550, '5.4.5 Daily sending quota exceeded')`

**Solutions:**
1. ✅ Reduce `LIMIT` in `send_email.py`
2. ✅ Wait 24 hours before trying again
3. ✅ Gmail limits:
   - Free accounts: ~500 emails/day
   - Google Workspace: ~2,000 emails/day

#### 🔴 CSV File Not Found

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'emails.csv'`

**Solutions:**
1. ✅ Ensure `emails.csv` exists in the same directory
2. ✅ Check file name spelling (case-sensitive)
3. ✅ Run script from correct directory:
   ```bash
   cd /path/to/email-automation
   python send_email.py
   ```

#### 🔴 Resume Attachment Error

**Error:** `FileNotFoundError: [Errno 2] No such file or directory: 'resume.pdf'`

**Solutions:**
1. ✅ Place `resume.pdf` in project root
2. ✅ Check file name matches `ATTACHMENT_PATH` variable
3. ✅ Verify file isn't corrupted

#### 🔴 GitHub Actions Not Running

**Problem:** Scheduled workflow doesn't trigger

**Solutions:**
1. ✅ Check if repository is public (or Actions enabled for private)
2. ✅ Verify secrets are set correctly
3. ✅ Ensure workflow file is in `.github/workflows/`
4. ✅ Check GitHub Actions tab for errors
5. ✅ Workflows may be disabled if no commits for 60 days

#### 🔴 Emails Going to Spam

**Problem:** Recipients not receiving or emails in spam folder

**Solutions:**
1. ✅ Avoid spam trigger words (FREE, URGENT, $$$)
2. ✅ Keep formatting simple (no excessive styling)
3. ✅ Add proper signature with contact info
4. ✅ Personalize each email
5. ✅ Test with [Mail Tester](https://www.mail-tester.com/)
6. ✅ Reduce sending rate

---

## 🏗️ Architecture

### System Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                     EMAIL AUTOMATION SYSTEM                  │
└─────────────────────────────────────────────────────────────┘

┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│  emails.csv  │────────▶│ send_email.py│────────▶│  Gmail SMTP  │
│  (contacts)  │         │  (Initial)   │         │   Server     │
└──────────────┘         └──────────────┘         └──────────────┘
                                │                          │
                                │                          ▼
                                ▼                  ┌──────────────┐
                         ┌──────────────┐         │  Recipients  │
                         │ sent_log.csv │         └──────────────┘
                         │  (tracking)  │
                         └──────────────┘
                                │
                                │ (after 3-5 days)
                                ▼
                         ┌──────────────┐
                         │send_followup │
                         │     .py      │
                         └──────────────┘
                                │
                                ▼
                         ┌──────────────┐
                         │followup_sent │
                         │    .csv      │
                         └──────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS LAYER                     │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐                    ┌──────────────┐       │
│  │   Cron Job   │                    │   Manual     │       │
│  │ Daily 3:30AM │────────┐  ┌───────▶│   Trigger    │       │
│  └──────────────┘        │  │        └──────────────┘       │
│                          ▼  ▼                                │
│                   ┌─────────────┐                            │
│                   │   Workflow  │                            │
│                   │   Executor  │                            │
│                   └─────────────┘                            │
│                          │                                   │
│                          ▼                                   │
│                   ┌─────────────┐                            │
│                   │ Auto-commit │                            │
│                   │  CSV Logs   │                            │
│                   └─────────────┘                            │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1️⃣ **send_email.py** - Initial Email Sender

**Purpose:** Send first-time job applications

**Process:**
```python
1. Load emails.csv
2. Load sent_log.csv (sent history)
3. Filter out already-sent emails
4. For each pending email (up to LIMIT):
   a. Generate personalized body
   b. Pick random subject & signature
   c. Attach resume.pdf
   d. Send via Gmail SMTP
   e. Log to sent_log.csv
   f. Sleep for random delay (50-120s)
```

**Key Variables:**
- `LIMIT = 125` - Max emails per run
- `MIN_DELAY = 50` - Minimum wait time
- `MAX_DELAY = 120` - Maximum wait time

#### 2️⃣ **send_followup.py** - Follow-up Sender

**Purpose:** Send follow-ups to non-responders

**Process:**
```python
1. Load sent_log.csv (who was emailed)
2. Load replied.csv (who responded)
3. Load followup_sent.csv (who got follow-up)
4. Calculate: pending = sent - replied - followed_up
5. For each pending (up to FOLLOWUP_LIMIT):
   a. Generate follow-up body
   b. Pick random subject & body variant
   c. Send via Gmail SMTP
   d. Log to followup_sent.csv
   e. Sleep for random delay (40-60s)
```

**Key Variables:**
- `FOLLOWUP_LIMIT = 40` - Max follow-ups per run
- `MIN_DELAY = 40` - Minimum wait time
- `MAX_DELAY = 60` - Maximum wait time

#### 3️⃣ **GitHub Actions Workflows**

**Workflow 1: send-emails.yml**
- Triggers daily at 3:30 AM UTC
- Can be manually triggered
- Runs `send_email.py` on GitHub servers
- Auto-commits updated logs

**Workflow 2: send_followups.yml**
- Manual trigger only (you control timing)
- Runs `send_followup.py` on GitHub servers
- Auto-commits updated logs

### Data Flow

```
emails.csv ──┐
             ├──▶ send_email.py ──▶ sent_log.csv ──┐
resume.pdf ──┘                                      │
                                                    ├──▶ send_followup.py ──▶ followup_sent.csv
replied.csv (optional) ─────────────────────────────┘
```

### File Dependencies

| File | Purpose | Created By | Read By |
|------|---------|-----------|---------|
| `emails.csv` | Contact list | You | send_email.py, send_followup.py |
| `sent_log.csv` | Sent tracking | send_email.py | send_email.py, send_followup.py |
| `followup_sent.csv` | Follow-up tracking | send_followup.py | send_followup.py |
| `replied.csv` | Response tracking | You (optional) | send_followup.py |
| `resume.pdf` | Resume attachment | You | send_email.py |

---

## 🤝 Contributing

We welcome contributions! Here's how you can help:

### 🌟 How to Contribute

1. **Fork the repository**
   ```bash
   # Click "Fork" button on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/your-username/email-automation.git
   cd email-automation
   ```

3. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

4. **Make your changes**
   - Write clean, documented code
   - Follow existing code style
   - Test thoroughly

5. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: amazing new feature"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/amazing-feature
   ```

7. **Open a Pull Request**
   - Go to original repository on GitHub
   - Click "New Pull Request"
   - Describe your changes

### 💡 Contribution Ideas

- 🎨 Add email templates for different industries
- 📊 Build analytics dashboard
- 🔍 Add email validation before sending
- 📧 Support for other email providers (Outlook, Yahoo)
- 🌐 Web UI for managing contacts
- 📱 Mobile app integration
- 🧪 Unit tests
- 📝 More documentation
- 🌍 Internationalization

### 🐛 Reporting Bugs

Found a bug? Please open an issue with:

- **Description:** What happened?
- **Expected behavior:** What should happen?
- **Steps to reproduce:** How can we recreate it?
- **Environment:** OS, Python version, etc.
- **Logs:** Relevant error messages

### 💬 Discussion

- 💡 Feature requests
- ❓ Questions
- 🎓 Tutorials
- 📚 Documentation improvements

---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2024 Email Automation Tool

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## ⚠️ Disclaimer

### Important Legal Notice

This tool is provided for **educational purposes** and **legitimate job application outreach only**.

#### ✅ Acceptable Use

- Sending genuine job applications to relevant contacts
- Following up on your own applications
- Contacting publicly listed recruiters with relevant opportunities

#### ❌ Unacceptable Use

- Mass spamming
- Sending unsolicited commercial emails
- Harvesting emails without consent
- Violating email service provider terms
- Ignoring unsubscribe/opt-out requests

### 📢 Responsibility

**You are solely responsible for:**
- Ensuring compliance with local laws (CAN-SPAM, GDPR, CASL)
- Obtaining proper consent for contacting individuals
- Respecting Gmail's terms of service and sending limits
- Honoring unsubscribe and opt-out requests
- Maintaining ethical email practices

**The authors and contributors:**
- Provide this tool "as-is" without warranties
- Are not liable for misuse or damages
- Do not endorse spamming or unethical practices
- Recommend consulting legal counsel for compliance

### 🛡️ Gmail Terms of Service

By using this tool, you agree to comply with:
- [Gmail Program Policies](https://support.google.com/mail/answer/81126)
- [Google's Acceptable Use Policy](https://policies.google.com/terms)
- Sending limits and rate restrictions

**⚠️ Violation may result in account suspension or termination.**

### 🌍 International Laws

Different countries have different email regulations:

| Region | Law | Key Requirements |
|--------|-----|-----------------|
| 🇺🇸 USA | CAN-SPAM Act | Include physical address, honor opt-outs within 10 days |
| 🇪🇺 EU | GDPR | Obtain explicit consent, provide data protection |
| 🇨🇦 Canada | CASL | Get consent before sending, include unsubscribe |
| 🇦🇺 Australia | Spam Act 2003 | Consent required, clear sender identification |

**Consult local laws before using this tool internationally.**

---

## 🙏 Acknowledgments

Built with ❤️ for job seekers who want to work smarter, not harder.

### 🔧 Technologies Used

- **Python 3** - Core programming language
- **Pandas** - CSV data manipulation
- **smtplib** - Email sending protocol
- **Gmail SMTP** - Email delivery service
- **GitHub Actions** - Automation and scheduling

### 📚 Resources

- [Python smtplib Documentation](https://docs.python.org/3/library/smtplib.html)
- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [CAN-SPAM Act Compliance](https://www.ftc.gov/tips-advice/business-center/guidance/can-spam-act-compliance-guide-business)

---

## 📞 Support & Contact

### Need Help?

- 📖 Read the [Troubleshooting](#-troubleshooting) section
- 💬 Open an [Issue](https://github.com/yourusername/email-automation/issues)
- 📧 Contact: your-email@example.com
- 🌐 Website: [yourwebsite.com](https://yourwebsite.com)

### 🔗 Links

- 🏠 [GitHub Repository](https://github.com/yourusername/email-automation)
- 📊 [Project Board](https://github.com/yourusername/email-automation/projects)
- 🐛 [Report Bug](https://github.com/yourusername/email-automation/issues/new?template=bug_report.md)
- 💡 [Request Feature](https://github.com/yourusername/email-automation/issues/new?template=feature_request.md)

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

**Made with 💻 and ☕ by job seekers, for job seekers**

[![GitHub stars](https://img.shields.io/github/stars/yourusername/email-automation?style=social)](https://github.com/yourusername/email-automation/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/email-automation?style=social)](https://github.com/yourusername/email-automation/network/members)
[![GitHub issues](https://img.shields.io/github/issues/yourusername/email-automation)](https://github.com/yourusername/email-automation/issues)

**Happy Job Hunting! 🚀**

</div>

---

<div align="center">
<sub>Last Updated: December 2024 | Version 1.0.0</sub>
</div>