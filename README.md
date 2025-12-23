# 📧 Career Outreach Emailer System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)
[![GitHub Actions](https://img.shields.io/badge/GitHub-Actions-2088FF?logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Gmail](https://img.shields.io/badge/Gmail-Powered-EA4335?logo=gmail&logoColor=white)](https://mail.google.com/)

> 🚀 **A fully automated email outreach system powered by GitHub Actions** - Send personalized emails, follow-ups, check for bounces and replies automatically!

## ✨ Features

- 📂 **Centralized Config** - All templates and settings in `email_config.py`
- 📬 **Automated Outreach** - Send personalized emails in batches
- 🔄 **Smart Follow-ups** - Automatic reminders to non-responders
- ❌ **Bounce Detection** - Automatically detect and log bounced emails
- 📥 **Reply Detection** - Automatically stop follow-ups when someone replies
- 🧪 **Dry Run Mode** - Preview emails with `--dry-run` before sending
- 📊 **Campaign Stats** - Real-time statistics on your outreach progress
- 📝 **Persistent Logging** - Detailed logs in `outreach.log`
- 🎲 **Content Randomization** - Avoid spam filters with varied templates
- 🔒 **Secure** - Uses GitHub Secrets for credential management

---

## 📋 Table of Contents

- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Getting Started](#-getting-started)
- [Configuration Options](#-configuration-options)
- [Managing Responses](#-managing-responses)
- [Statistics](#-statistics)
- [Troubleshooting](#-troubleshooting)

---

## 🔍 How It Works

This system uses **GitHub Actions** to automatically send emails on a schedule:

1. 📅 **Outreach**: Runs daily to send new emails.
2. 🔄 **Follow-up**: Sends polite reminders to those who haven't replied.
3. 🔎 **Monitors**: `bounce_checker.py` and `reply_checker.py` keep your lists clean.
4. 💾 **Sync**: Automatically commits tracking data back to your repository.

---

## 📂 Project Structure

- `email_config.py`: **Main Configuration**. Edit templates and limits here.
- `send_email.py`: Sends initial outreach emails.
- `send_followup.py`: Sends follow-up emails.
- `reply_checker.py`: Checks inbox for replies and updates `replied.csv`.
- `bounce_checker.py`: Scans for delivery failures and updates `bounced_emails.csv`.
- `stats.py`: Provides a summary of your campaign.
- `mailer.py`: Shared utilities for SMTP and logging.
- `emails.csv`: Your target recipient list.
- `outreach.log`: Detailed execution logs.

---

## 🚀 Getting Started

### 1. Fork and Setup
1. Fork this repository.
2. In **Settings > Secrets > Actions**, add:
   - `EMAIL_ADDRESS`: Your Gmail.
   - `EMAIL_PASSWORD`: Your 16-character [Gmail App Password](https://myaccount.google.com/apppasswords).

### 2. Customize Content
Edit [email_config.py](email_config.py) to change:
- `INITIAL_SUBJECTS`, `INITIAL_BODY_TEMPLATE`
- `FOLLOWUP_SUBJECTS`, `FOLLOWUP_BODY_VARIANTS`
- `LINKS`, `ATTACHMENT_PATH` (upload your resume too!)

### 3. Run a Test
Execute `send_email.py` with the dry-run flag to see what would be sent:
```bash
python send_email.py --dry-run
```

---

## ⚙️ Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `CHECK_DAYS_BACK` | How far back to check for replies/bounces | 20 |
| `INITIAL_LIMIT` | Max outreach emails per run | 100 |
| `FOLLOWUP_LIMIT` | Max follow-up emails per run | 40 |
| `RUN_FOLLOWUP_AUTO` | Enable automated follow-ups in Actions | False |

---

## 📬 Managing Responses

### 📝 Tracking Responses Manually

When someone replies to your email, you need to manually update `replied.csv` to prevent follow-ups.

#### **Creating/Updating `replied.csv`:**

1. If `replied.csv` doesn't exist, create it in your repository
2. Click **"Add file"** → **"Create new file"**
3. Name it: `replied.csv`
4. Add this header:
   ```csv
   email
   ```
5. Add responded email addresses (one per line):
   ```csv
   email
   john.doe@company.com
   jane.smith@business.org
   ```
6. Commit the file

---

### 🔄 How It Works:

- The `send_followup.py` script checks `replied.csv`
- Emails in this file will **NOT** receive follow-ups
- This prevents bothering people who already responded

---

### 📊 Tracking Status:

| File | Purpose | Updated By |
|------|---------|-----------|
| `emails.csv` | Master contact list | You (manual) |
| `sent_log.csv` | Tracks sent initial emails | Automated |
| `followup_sent.csv` | Tracks sent follow-ups | Automated |
| `replied.csv` | Tracks who replied | You (manual) |

---

### 🔍 Workflow:

```
emails.csv → send_email.py → sent_log.csv
                                   ↓
                              (Wait days)
                                   ↓
              (Check replied.csv for responses)
                                   ↓
              send_followup.py → followup_sent.csv
```

---

## 📊 Statistics

Run the stats script at any time to see your progress:
```bash
python stats.py
```
**Example Output:**
```text
==============================
      CAMPAIGN STATISTICS
==============================
Total Contacts:    500
Emails Sent:       150
Pending Outreach:  350
Follow-ups Sent:   40
------------------------------
Replies Detected:  12
Bounces Detected:  5
------------------------------
Reply Rate:        8.00%
Bounce Rate:       3.33%
==============================
```

---

## 🎮 Manual Execution

You can trigger any workflow manually from the **Actions** tab on GitHub:
1. Select a workflow (e.g., `Send Daily Emails`).
2. Click **Run workflow**.

---

## 🔧 Troubleshooting

- **Authentication Error**: Ensure you use an **App Password**, not your regular password.
- **Spam Issues**: Increase `INITIAL_MIN_DELAY` and `INITIAL_MAX_DELAY` in `email_config.py`.
- **Not Starting**: Ensure you've clicked "Enable Workflows" in the Actions tab.

---

## 📜 License
MIT License. Use responsibly.

---

## ⚠️ Disclaimer

**Use this tool responsibly:**
- 📋 Only send emails to people who expect to hear from you
- 🚫 Don't use for spam or unsolicited commercial emails
- ✅ Comply with CAN-SPAM Act, GDPR, and other email regulations
- 🤝 Respect recipient privacy and provide opt-out options
- ⚖️ You are responsible for how you use this tool

---

## 🌟 Show Your Support

If you found this project helpful:
- ⭐ **Star this repository**
- 🍴 **Fork it** and customize for your needs
- 📢 **Share** with others who might find it useful
- 🐛 **Report bugs** or **suggest improvements**

---

## 📞 Contact

Have questions? Need help?
- 📧 Open an issue on GitHub
- 💬 Check existing issues for solutions
- 📖 Read through this README carefully

---

<div align="center">

### 🚀 Ready to automate your outreach?

**[Fork This Repo](#step-1-fork-this-repository)** • **[Get Started](#-getting-started)** • **[Report Issues](https://github.com/yourusername/email-sender-automation/issues)**

---

**Made with ❤️ for efficient outreach campaigns**

*Last Updated: January 2025*

</div>
