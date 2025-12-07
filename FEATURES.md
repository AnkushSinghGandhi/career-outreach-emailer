# 🚀 New Features Guide

This document explains all the new features added to the Email Automation Tool.

---

## 📋 Table of Contents

1. [Configuration File System](#1-configuration-file-system-)
2. [Better Logging System](#2-better-logging-system-)
3. [Retry Mechanism](#3-retry-mechanism-)
4. [Progress Bar](#4-progress-bar-)
5. [Response Auto-Detector](#5-response-auto-detector-)
6. [Backup System](#6-backup-system-)
7. [Utility Scripts](#7-utility-scripts)

---

## 1. Configuration File System ⚙️

**File:** `config.yaml`

All settings are now centralized in a YAML configuration file instead of hardcoded values.

### Features:
- ✅ Email limits and delays
- ✅ SMTP server settings
- ✅ File paths
- ✅ Retry configuration
- ✅ Logging options
- ✅ Backup settings
- ✅ Response detection settings
- ✅ Progress bar customization

### Example Configuration:

```yaml
email:
  limit: 125                    # Daily sending limit
  min_delay: 50                 # Minimum delay (seconds)
  max_delay: 120                # Maximum delay (seconds)

retry:
  enabled: true
  max_attempts: 3               # Retry failed emails 3 times
  initial_delay: 5
  backoff_multiplier: 2         # Exponential backoff (5s, 10s, 20s)
```

### Usage:

```bash
# View current configuration
python view_config.py

# Edit configuration
nano config.yaml
```

---

## 2. Better Logging System 📊

**Module:** `logger_config.py`

Enhanced logging with timestamps, log levels, and file output.

### Features:
- ✅ Timestamped logs
- ✅ Log levels (DEBUG, INFO, WARNING, ERROR)
- ✅ Console and file output
- ✅ Separate log files per script
- ✅ Daily log rotation
- ✅ Color-coded console output

### Log Files Location:

```
logs/
├── send_email_20241207.log
├── send_followup_20241207.log
├── check_responses_20241207.log
└── manage_backups_20241207.log
```

### Log Format:

**Console:**
```
INFO: Starting email campaign
✓ Sent to: john@example.com
✗ Failed to send to invalid@email.com
```

**File:**
```
[2024-12-07 10:30:45] INFO - Starting email campaign
[2024-12-07 10:30:46] INFO - ✓ Sent to: john@example.com
[2024-12-07 10:32:10] ERROR - ✗ Failed to send to invalid@email.com
```

### Configuration:

```yaml
logging:
  enabled: true
  log_dir: logs
  log_level: INFO              # DEBUG, INFO, WARNING, ERROR
  console_output: true
  file_output: true
```

---

## 3. Retry Mechanism 🔄

**Feature:** Automatic retry with exponential backoff

### How It Works:

When an email fails to send, the system automatically retries with increasing delays:

```
Attempt 1: Send → Fail
Wait 5 seconds...
Attempt 2: Send → Fail
Wait 10 seconds...
Attempt 3: Send → Success ✓
```

### Configuration:

```yaml
retry:
  enabled: true
  max_attempts: 3               # Total attempts (including first try)
  initial_delay: 5              # First retry after 5 seconds
  backoff_multiplier: 2         # Double delay each time
```

### Backoff Calculation:

- Attempt 1 (initial): Immediate
- Attempt 2: 5 seconds
- Attempt 3: 10 seconds (5 × 2)
- Attempt 4: 20 seconds (10 × 2)

### Benefits:

- ✅ Handles temporary network issues
- ✅ Prevents immediate failure on transient errors
- ✅ Increases success rate
- ✅ Configurable retry behavior

### Example Output:

```
INFO: Sending to john@example.com...
WARNING: Attempt 1 failed for john@example.com. Retrying in 5s...
WARNING: Attempt 2 failed for john@example.com. Retrying in 10s...
✓ Sent to: john@example.com
```

---

## 4. Progress Bar ⏳

**Library:** `tqdm`

Visual progress indicator with ETA and statistics.

### Features:
- ✅ Real-time progress
- ✅ Estimated time remaining (ETA)
- ✅ Speed indicator
- ✅ Current delay display
- ✅ Color-coded bar
- ✅ Clean output

### Example Output:

```
Sending emails: [████████████░░░░░░░░] 60% | 75/125 [01:45<01:10]
```

### Components:
- `60%` - Progress percentage
- `75/125` - Current/Total emails
- `01:45` - Time elapsed
- `01:10` - Time remaining (ETA)

### Configuration:

```yaml
progress:
  enabled: true
  show_eta: true
  color: green                  # green, blue, red, yellow, etc.
```

### Disable Progress Bar:

Set `enabled: false` in config.yaml for minimal output.

---

## 5. Response Auto-Detector 🤖

**Module:** `response_detector.py`

Automatically detect email responses using Gmail IMAP.

### Features:
- ✅ Auto-check Gmail for replies
- ✅ Update `replied.csv` automatically
- ✅ Skip follow-ups for responders
- ✅ Response statistics
- ✅ Configurable check period

### How It Works:

1. Connects to Gmail via IMAP
2. Searches for emails from contacts you emailed
3. Identifies new responses
4. Updates `replied.csv`
5. Prevents follow-ups to responders

### Configuration:

```yaml
response_detection:
  enabled: false                # Set to true to enable
  check_days: 7                 # Check last 7 days
  auto_update_replied: true     # Auto-update replied.csv
```

### Enable IMAP in Gmail:

1. Go to [Gmail Settings](https://mail.google.com/mail/u/0/#settings/fwdandpop)
2. Click **Forwarding and POP/IMAP**
3. Enable **IMAP access**
4. Click **Save Changes**

### Usage:

**Automatic (runs before sending):**
```bash
# If enabled in config, automatically checks before sending
python send_email_v2.py
```

**Manual check:**
```bash
python check_responses.py
```

### Example Output:

```
Email Response Checker
==================================================
Checking Gmail for responses...
✓ Found 3 new responses!

  1. john@example.com
     Replied on: 2024-12-07 14:30:00
     Subject: Re: Application for Python Developer Role

  2. jane@startup.io
     Replied on: 2024-12-07 15:15:00
     Subject: Re: Interest in Backend Opportunities

==================================================
Response Statistics:
==================================================
  Total Sent:      125
  Total Replied:   8
  No Response:     117
  Response Rate:   6.4%
```

### Response Statistics:

```python
# Get stats programmatically
from response_detector import ResponseDetector

detector = ResponseDetector()
stats = detector.get_response_stats()

print(f"Response Rate: {stats['response_rate']}%")
```

---

## 6. Backup System 💾

**Module:** `backup_manager.py`

Automatic backups of CSV files before each run.

### Features:
- ✅ Auto-backup before sending
- ✅ Timestamped backup folders
- ✅ Configurable retention
- ✅ Easy restore
- ✅ Manual backup creation
- ✅ Backup listing

### Backup Structure:

```
backups/
├── backup_20241207_103045/
│   ├── sent_log.csv
│   ├── followup_sent.csv
│   ├── emails.csv
│   └── replied.csv
├── backup_20241207_153022/
└── backup_20241207_200015/
```

### Configuration:

```yaml
backup:
  enabled: true
  backup_dir: backups
  keep_last: 10                 # Keep only 10 most recent
  backup_before_run: true       # Auto-backup before sending
```

### Usage:

**Automatic (runs before sending):**
```bash
# Automatically creates backup if enabled
python send_email_v2.py
```

**Manual Commands:**

```bash
# List all backups
python manage_backups.py list

# Create manual backup
python manage_backups.py create

# Restore from backup
python manage_backups.py restore backups/backup_20241207_103045

# View help
python manage_backups.py help
```

### Example Output:

**List backups:**
```
Found 5 backup(s):

  1. 2024-12-07 20:00:15
     Path: backups/backup_20241207_200015

  2. 2024-12-07 15:30:22
     Path: backups/backup_20241207_153022

  3. 2024-12-07 10:30:45
     Path: backups/backup_20241207_103045
```

**Create backup:**
```
Creating backup...
✓ Backup created: backups/backup_20241207_210030
Files backed up: 4
  - sent_log.csv
  - followup_sent.csv
  - emails.csv
  - replied.csv
```

**Restore backup:**
```
Restoring from: backups/backup_20241207_103045
✓ Restored 4 file(s):
  - sent_log.csv
  - followup_sent.csv
  - emails.csv
  - replied.csv
```

### Automatic Cleanup:

Old backups are automatically removed, keeping only the configured number of recent backups.

---

## 7. Utility Scripts

### 7.1 View Configuration

**Script:** `view_config.py`

Display current configuration with status indicators.

```bash
python view_config.py
```

**Output:**
```
Email Automation Configuration
============================================================

📧 EMAIL SETTINGS
────────────────────────────────────────────────────────────
  Daily Limit:           125 emails
  Follow-up Limit:       40 emails
  Delay Range:           50-120 seconds
  SMTP Server:           smtp.gmail.com:587

📁 FILE SETTINGS
────────────────────────────────────────────────────────────
  contacts             ✓ emails.csv
  sent_log             ✓ sent_log.csv
  followup_sent        ✓ followup_sent.csv
  replied              ✗ replied.csv
  resume               ✓ resume.pdf

🔄 RETRY SETTINGS
────────────────────────────────────────────────────────────
  Status:                Enabled
  Max Attempts:          3
  Initial Delay:         5 seconds
  Backoff Multiplier:    2x

[... more sections ...]
```

### 7.2 Check Responses

**Script:** `check_responses.py`

Manually check for email responses.

```bash
python check_responses.py
```

### 7.3 Manage Backups

**Script:** `manage_backups.py`

Manage CSV backups.

```bash
# List backups
python manage_backups.py list

# Create backup
python manage_backups.py create

# Restore backup
python manage_backups.py restore backups/backup_20241207_103045
```

---

## 🚀 Using the New Scripts

### Original Scripts (Still Work):
```bash
python send_email.py        # Old version
python send_followup.py     # Old version
```

### New Enhanced Scripts:
```bash
python send_email_v2.py     # New version with all features
python send_followup_v2.py  # New version with all features
```

### Comparison:

| Feature | Original | Enhanced (v2) |
|---------|----------|---------------|
| Basic sending | ✅ | ✅ |
| CSV tracking | ✅ | ✅ |
| Configuration file | ❌ | ✅ |
| Enhanced logging | ❌ | ✅ |
| Retry mechanism | ❌ | ✅ |
| Progress bar | ❌ | ✅ |
| Response detection | ❌ | ✅ |
| Auto-backup | ❌ | ✅ |

---

## 📖 Quick Start with New Features

### 1. Setup Configuration

```bash
# View and verify configuration
python view_config.py

# Edit if needed
nano config.yaml
```

### 2. Set Environment Variables

```bash
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

### 3. Enable Response Detection (Optional)

Edit `config.yaml`:
```yaml
response_detection:
  enabled: true  # Change to true
```

Enable IMAP in Gmail settings.

### 4. Run Enhanced Scripts

```bash
# Send emails with all new features
python send_email_v2.py

# Send follow-ups with all new features
python send_followup_v2.py
```

### 5. Monitor and Manage

```bash
# Check responses
python check_responses.py

# List backups
python manage_backups.py list

# View logs
cat logs/send_email_20241207.log
```

---

## 🎯 Benefits Summary

| Feature | Benefit |
|---------|---------|
| **Config File** | Easy customization without code changes |
| **Better Logging** | Track everything, debug issues faster |
| **Retry Mechanism** | Higher success rate, fewer failures |
| **Progress Bar** | Visual feedback, know when it'll finish |
| **Response Detector** | Auto-track replies, avoid annoying responders |
| **Backup System** | Never lose data, easy recovery |

---

## ⚠️ Important Notes

1. **Original scripts still work** - `send_email.py` and `send_followup.py` remain unchanged
2. **Use v2 scripts for new features** - `send_email_v2.py` and `send_followup_v2.py`
3. **Response detection requires IMAP** - Enable in Gmail settings
4. **Backups are automatic** - No manual intervention needed
5. **Logs rotate daily** - One file per script per day

---

## 🔧 Troubleshooting

### Issue: Response detection not working

**Solution:**
1. Enable IMAP in Gmail
2. Verify credentials are correct
3. Check `config.yaml` has `enabled: true`

### Issue: Progress bar not showing

**Solution:**
Check `config.yaml`:
```yaml
progress:
  enabled: true
```

### Issue: Backups not created

**Solution:**
Check `config.yaml`:
```yaml
backup:
  enabled: true
  backup_before_run: true
```

### Issue: Retry not working

**Solution:**
Check `config.yaml`:
```yaml
retry:
  enabled: true
```

---

## 📚 Additional Resources

- **Configuration Reference:** `config.yaml`
- **Module Documentation:** See individual `.py` files
- **Main README:** `README.md`
- **GitHub Actions:** `.github/workflows/`

---

**Happy Emailing! 🚀**
