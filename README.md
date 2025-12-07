# 📧 Email Automation System for Job Applications

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?style=for-the-badge&logo=github-actions&logoColor=white)
![Status](https://img.shields.io/badge/Status-Production_Ready-success?style=for-the-badge)

**Fully automated email campaign system with test mode, retry logic, and comprehensive tracking**

[Features](#-features) • [Quick Start](#-quick-start) • [Usage](#-usage) • [Workflows](#-github-actions-workflows)

</div>

---

## 📖 Table of Contents

- [✨ Features](#-features)
- [🏗️ Architecture](#️-architecture)
- [⚡ Quick Start](#-quick-start)
- [🔧 Configuration](#-configuration)
- [📊 CSV Files](#-csv-files)
- [💻 Usage](#-usage)
  - [Test Mode](#test-mode)
  - [Production Mode](#production-mode)
- [🤖 GitHub Actions Workflows](#-github-actions-workflows)
- [📚 Scripts Reference](#-scripts-reference)
- [🛡️ Best Practices](#️-best-practices)
- [🐛 Troubleshooting](#-troubleshooting)

---

## ✨ Features

### 🎯 Core Capabilities

| Feature | Description |
|---------|-------------|
| 🧪 **Test Mode** | Safe testing with test_emails.csv before production |
| 🔄 **Smart Follow-ups** | Automatically follow up with non-responders |
| 🎲 **Anti-Spam Protection** | Randomized subjects, delays, and content |
| 🔁 **Retry Logic** | Exponential backoff for failed sends |
| 📊 **Progress Tracking** | Real-time progress bars and statistics |
| 💾 **Auto Backup** | Automatic CSV backups before each run |
| 📝 **Comprehensive Logging** | Detailed logs for debugging and auditing |
| 🤖 **GitHub Actions** | Fully automated with scheduled and manual workflows |
| 📧 **Response Detection** | (Optional) Auto-detect replies via IMAP |

### 🎭 Dual Mode System

- **Test Mode**: Use test_emails.csv with low limits (5 emails, 10-20s delays)
- **Production Mode**: Use emails.csv with production limits (125 emails, 50-120s delays)

---

## 🏗️ Architecture

```
📦 Email Automation System
├── 📄 Configuration
│   └── config.yaml                    # Central configuration file
│
├── 🗂️ Production Files
│   ├── emails.csv                     # Main contact list
│   ├── sent_log.csv                   # Sent tracking
│   ├── followup_sent.csv              # Follow-up tracking
│   └── replied.csv                    # Response tracking
│
├── 🧪 Test Files
│   ├── test_emails.csv                # Test contact list
│   ├── test_sent_log.csv              # Test sent tracking
│   ├── test_followup_sent.csv         # Test follow-up tracking
│   └── test_replied.csv               # Test response tracking
│
├── 🐍 Core Scripts
│   ├── send_email_v2.py               # Enhanced email sender
│   └── send_followup_v2.py            # Enhanced follow-up sender
│
├── 🔧 Supporting Modules
│   ├── backup_manager.py              # CSV backup system
│   ├── logger_config.py               # Custom logging
│   └── response_detector.py           # IMAP response detection
│
└── 🤖 GitHub Actions Workflows
    ├── send-emails.yml                # Production: Daily emails
    ├── send_followups.yml             # Production: Follow-ups
    ├── test-send-emails.yml           # Test: Email testing
    └── test-send-followups.yml        # Test: Follow-up testing
```

---

## ⚡ Quick Start

### 1️⃣ Initial Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd email-automation

# Install dependencies
pip install pandas pyyaml tqdm

# Set environment variables
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-16-char-app-password"
```

### 2️⃣ Configure Gmail App Password

1. Enable **2-Step Verification** in Google Account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Generate password for "Mail" → "Other (Custom name)"
4. Copy the 16-character password

### 3️⃣ Add GitHub Secrets (for automation)

Go to: **Repository → Settings → Secrets and variables → Actions**

Add these secrets:
- `EMAIL_ADDRESS`: your-email@gmail.com
- `EMAIL_PASSWORD`: your-16-char-app-password

---

## 🔧 Configuration

All settings are in **`config.yaml`**:

```yaml
email:
  limit: 125                    # Max emails per run
  followup_limit: 40            # Max follow-ups per run
  min_delay: 50                 # Min delay (seconds)
  max_delay: 120                # Max delay (seconds)

test_mode:
  enabled: false                # Enable test mode by default
  test_contacts: test_emails.csv
  limit: 5                      # Lower limit for testing
  min_delay: 10                 # Shorter delays for testing

retry:
  enabled: true
  max_attempts: 3               # Retry failed emails 3 times

backup:
  enabled: true
  backup_before_run: true       # Backup CSVs before each run
  keep_last: 10                 # Keep last 10 backups

logging:
  log_level: INFO
  console_output: true
  file_output: true
```

**Key Settings:**
- Adjust `limit` to control daily email volume
- Adjust `min_delay`/`max_delay` to control sending pace
- Enable `response_detection` for automatic reply tracking (requires IMAP)

---

## 📊 CSV Files

### Production Files

#### `emails.csv` (Your main contact list)
```csv
email,first_name
john.doe@company.com,John
jane.smith@startup.io,Jane
recruiter@techcorp.com,Sarah
```

#### `sent_log.csv` (Auto-generated)
Tracks all sent emails to prevent duplicates.

#### `followup_sent.csv` (Auto-generated)
Tracks follow-up emails sent.

#### `replied.csv` (Manual/Auto)
Add emails of people who replied to skip them from follow-ups.

```csv
email
jane.smith@startup.io
```

### Test Files

#### `test_emails.csv` (Your test contacts)
```csv
email,first_name
test1@example.com,Alice
test2@example.com,Bob
your-test-email@gmail.com,Test User
```

**Test files work independently from production files.**

---

## 💻 Usage

### 🧪 Test Mode

**Use test mode to verify everything works before production.**

#### Local Testing

```bash
# Test email sending (uses test_emails.csv)
python send_email_v2.py --test-mode

# Dry run (no emails sent, just simulation)
python send_email_v2.py --test-mode --dry-run

# Test follow-ups
python send_followup_v2.py --test-mode
```

#### GitHub Actions Testing

1. Go to **Actions** tab in GitHub
2. Select **"Test - Send Emails"** workflow
3. Click **Run workflow**
4. Choose:
   - `dry_run: false` → Actually send test emails
   - `dry_run: true` → Simulate without sending

**Test workflows:**
- ✅ Use `test_emails.csv`
- ✅ Send only 5 emails (configurable in config.yaml)
- ✅ Use shorter delays (10-20s)
- ✅ Auto-commit test logs
- ✅ No scheduled runs (manual only)

---

### 🚀 Production Mode

**For actual job applications to real contacts.**

#### Local Production Run

```bash
# Send initial emails (uses emails.csv)
python send_email_v2.py

# Send follow-ups
python send_followup_v2.py

# Dry run
python send_email_v2.py --dry-run
```

#### GitHub Actions Production

**Automated daily sending:**

1. **Daily Email Campaign** (Automated)
   - Workflow: `send-emails.yml`
   - Schedule: Daily at 3:30 AM UTC
   - Sends up to 125 emails per day
   - Auto-commits logs

2. **Manual Follow-ups**
   - Go to **Actions** → **"Send Follow-up Emails"**
   - Click **Run workflow**
   - Sends up to 40 follow-ups

**Production workflows:**
- ✅ Use `emails.csv`
- ✅ Production limits (125 initial, 40 follow-ups)
- ✅ Longer delays (50-120s)
- ✅ Auto-commit logs
- ✅ Daily schedule (can be disabled)

---

## 🤖 GitHub Actions Workflows

### Production Workflows

#### 1. 📨 Daily Email Sender (`send-emails.yml`)

**Trigger:**
- 🕒 **Scheduled**: Daily at 3:30 AM UTC
- 🖱️ **Manual**: Click "Run workflow"

**What it does:**
```
1. Checks out repository
2. Installs Python 3.10 + dependencies
3. Runs send_email.py (uses emails.csv)
4. Auto-commits updated sent_log.csv
```

**Usage:**
- Runs automatically every day
- Disable schedule by removing `schedule:` section

#### 2. 📬 Follow-up Sender (`send_followups.yml`)

**Trigger:**
- 🖱️ **Manual only**

**What it does:**
```
1. Identifies emails sent but not replied
2. Sends follow-up emails (up to 40)
3. Auto-commits followup_sent.csv
```

**Usage:**
- Go to Actions → "Send Follow-up Emails" → Run workflow
- Recommended: Run 3-5 days after initial campaign

---

### Test Workflows

#### 3. 🧪 Test Email Sender (`test-send-emails.yml`)

**Trigger:**
- 🖱️ **Manual only**
- 🎛️ Option: `dry_run` (true/false)

**What it does:**
```
1. Runs send_email_v2.py --test-mode
2. Uses test_emails.csv
3. Sends max 5 emails with 10-20s delays
4. Auto-commits test_sent_log.csv
```

**Usage:**
```
Actions → "Test - Send Emails" → Run workflow
├── dry_run: false → Actually send to test_emails.csv
└── dry_run: true  → Simulate without sending
```

#### 4. 🧪 Test Follow-up Sender (`test-send-followups.yml`)

**Trigger:**
- 🖱️ **Manual only**
- 🎛️ Option: `dry_run` (true/false)

**What it does:**
```
1. Runs send_followup_v2.py --test-mode
2. Uses test files
3. Sends test follow-ups
4. Auto-commits test logs
```

**Usage:**
- First run test email sender to populate test_sent_log.csv
- Then run test follow-up sender

---

## 📚 Scripts Reference

### Core Scripts

#### `send_email_v2.py` (Enhanced Email Sender)

**Features:**
- ✅ Test mode support
- ✅ Retry logic with exponential backoff
- ✅ Progress bars
- ✅ Automatic backups
- ✅ Comprehensive logging
- ✅ Response detection

**CLI Options:**
```bash
python send_email_v2.py                 # Production mode
python send_email_v2.py --test-mode     # Test mode
python send_email_v2.py --dry-run       # Dry run
```

#### `send_followup_v2.py` (Enhanced Follow-up Sender)

**Features:**
- ✅ Test mode support
- ✅ Smart filtering (skip replied emails)
- ✅ Retry logic
- ✅ Progress tracking

**CLI Options:**
```bash
python send_followup_v2.py                 # Production mode
python send_followup_v2.py --test-mode     # Test mode
python send_followup_v2.py --dry-run       # Dry run
```

### Legacy Scripts

#### `send_email.py` & `send_followup.py`

Original simple versions without advanced features. Still functional but v2 scripts recommended.

---

## 🛡️ Best Practices

### 🎯 Email Strategy

| Practice | Why It Matters |
|----------|---------------|
| 🧪 **Always test first** | Use test mode before production |
| 📊 **Track responses** | Update replied.csv to avoid annoying responders |
| ⏰ **Space out follow-ups** | Wait 3-5 days before following up |
| 📝 **Personalize content** | Better response rates |
| 🎲 **Use randomization** | Avoid spam filters |

### 🔒 Security

✅ **DO:**
- Use app-specific passwords (not main password)
- Store credentials in environment variables
- Keep test and production files separate
- Enable 2FA on Gmail

❌ **DON'T:**
- Commit credentials to Git
- Share app passwords
- Exceed Gmail's daily limits
- Ignore bounce emails

### 📈 Optimization

1. **Start Small**: Begin with 20-30 emails/day with new accounts
2. **Test Everything**: Use test mode extensively
3. **Monitor Metrics**: Track open rates and responses
4. **Adjust Timing**: Experiment with different send times
5. **Clean Lists**: Remove bounced emails regularly

---

## 🐛 Troubleshooting

### Common Issues

#### ❌ Authentication Failed

**Error:** `SMTPAuthenticationError: Username and Password not accepted`

**Solution:**
```bash
# Verify environment variables
echo $EMAIL_ADDRESS
echo $EMAIL_PASSWORD

# Ensure using App Password (16 chars), not regular password
# Regenerate App Password if needed
```

#### ❌ Daily Limit Exceeded

**Error:** `Daily sending quota exceeded`

**Solution:**
- Reduce `limit` in config.yaml
- Wait 24 hours before trying again
- Gmail limits: ~500/day (free), ~2000/day (Workspace)

#### ❌ File Not Found

**Error:** `FileNotFoundError: emails.csv`

**Solution:**
```bash
# Ensure you're in the correct directory
cd /path/to/email-automation

# Verify files exist
ls -la *.csv

# Check config.yaml file paths
cat config.yaml | grep -A 5 "files:"
```

#### ❌ GitHub Actions Not Running

**Problem:** Scheduled workflow doesn't trigger

**Solution:**
- Workflows disabled after 60 days of no commits
- Verify secrets are set correctly
- Check if repository is public (or Actions enabled for private)
- Manually trigger once to reactivate

#### ❌ Emails Going to Spam

**Solution:**
- Avoid spam trigger words (FREE, URGENT, $$$)
- Personalize each email
- Use proper signatures
- Test with [Mail Tester](https://www.mail-tester.com/)
- Reduce sending rate

---

## 📊 Workflow Diagram

```
┌─────────────────────────────────────────────────────┐
│                    TESTING PHASE                     │
├─────────────────────────────────────────────────────┤
│                                                       │
│  1. Add test emails to test_emails.csv              │
│  2. Run: Test - Send Emails (dry_run: true)         │
│  3. Verify logs and output                          │
│  4. Run: Test - Send Emails (dry_run: false)        │
│  5. Check if emails received correctly              │
│  6. Test follow-ups (if needed)                     │
│                                                       │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│                  PRODUCTION PHASE                    │
├─────────────────────────────────────────────────────┤
│                                                       │
│  1. Add contacts to emails.csv                      │
│  2. Configure config.yaml (limits, delays)          │
│  3. Set up GitHub Secrets                           │
│  4. Enable "Daily Email Sender" workflow            │
│     → Runs automatically every day                  │
│                                                       │
│  5. Wait 3-5 days                                   │
│  6. Update replied.csv with responses               │
│  7. Run "Send Follow-up Emails" manually            │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## 🎓 Usage Examples

### Example 1: Complete Test Run

```bash
# Step 1: Add test contacts
echo "email,first_name" > test_emails.csv
echo "test1@example.com,Alice" >> test_emails.csv
echo "test2@example.com,Bob" >> test_emails.csv

# Step 2: Dry run to verify
python send_email_v2.py --test-mode --dry-run

# Step 3: Actually send test emails
python send_email_v2.py --test-mode

# Step 4: Check test logs
cat test_sent_log.csv
```

### Example 2: Production Campaign

```bash
# Step 1: Prepare contacts
# Edit emails.csv with your contact list

# Step 2: Test configuration
python send_email_v2.py --dry-run

# Step 3: Send initial campaign
python send_email_v2.py

# Step 4: After 5 days, send follow-ups
python send_followup_v2.py
```

### Example 3: GitHub Actions

```bash
# Step 1: Set up secrets in GitHub
# EMAIL_ADDRESS, EMAIL_PASSWORD

# Step 2: Run test workflow
# Actions → "Test - Send Emails" → Run workflow (dry_run: true)

# Step 3: Review logs in Actions tab

# Step 4: Run production
# Actions → "Send Daily Emails" → Run workflow

# Step 5: Enable scheduled runs
# (Already enabled by default in send-emails.yml)
```

---

## 📞 Support

### Need Help?

- 📖 Read the [Troubleshooting](#-troubleshooting) section
- 💬 Open an [Issue](https://github.com/yourusername/email-automation/issues)
- 📧 Check logs in `logs/` directory

### 🔗 Resources

- [Gmail SMTP Settings](https://support.google.com/mail/answer/7126229)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Python smtplib Docs](https://docs.python.org/3/library/smtplib.html)

---

## ⚠️ Disclaimer

**This tool is for legitimate job application outreach only.**

### ✅ Acceptable Use
- Genuine job applications
- Following up on your applications
- Contacting publicly listed recruiters

### ❌ Prohibited Use
- Mass spamming
- Unsolicited commercial emails
- Violating email service provider terms
- Ignoring unsubscribe requests

**You are responsible for:**
- Complying with local laws (CAN-SPAM, GDPR, CASL)
- Respecting Gmail's terms of service
- Honoring opt-out requests
- Maintaining ethical email practices

**Gmail's daily limits:**
- Free accounts: ~500 emails/day
- Google Workspace: ~2,000 emails/day

Violating these limits may result in account suspension.

---

## 📄 License

MIT License - See LICENSE file for details

---

<div align="center">

### ⭐ Star this repository if you found it helpful!

**Made with 💻 and ☕ by job seekers, for job seekers**

**Happy Job Hunting! 🚀**

</div>

---

<div align="center">
<sub>Version 2.0.0 | Last Updated: 2024</sub>
</div>
