# 🚀 Quick Start Guide - Enhanced Features

## 📌 What's New?

Your email automation tool now has **6 powerful new features**:

1. ⚙️ **Configuration File** - Easy settings management
2. 📊 **Better Logging** - Track everything that happens
3. 🔄 **Retry Mechanism** - Auto-retry failed emails
4. ⏳ **Progress Bar** - Visual feedback with ETA
5. 🤖 **Response Detector** - Auto-detect replies
6. 💾 **Backup System** - Auto-backup CSV files

---

## ⚡ Quick Commands

### View Configuration
```bash
python view_config.py
```

### Send Emails (Enhanced Version)
```bash
python send_email_v2.py
```

### Send Follow-ups (Enhanced Version)
```bash
python send_followup_v2.py
```

### Check for Responses
```bash
python check_responses.py
```

### Manage Backups
```bash
# List all backups
python manage_backups.py list

# Create manual backup
python manage_backups.py create

# Restore from backup
python manage_backups.py restore backups/backup_20241207_103045
```

---

## 🎯 Using Enhanced Scripts

### Old Scripts (Still Work)
```bash
python send_email.py        # Original version
python send_followup.py     # Original version
```

### New Scripts (Recommended)
```bash
python send_email_v2.py     # ✅ With all new features
python send_followup_v2.py  # ✅ With all new features
```

---

## ⚙️ Quick Configuration

### Edit Settings
```bash
nano config.yaml
```

### Key Settings to Customize

**Email Limits:**
```yaml
email:
  limit: 125              # Change daily limit
  followup_limit: 40      # Change follow-up limit
```

**Delays:**
```yaml
email:
  min_delay: 50           # Minimum wait (seconds)
  max_delay: 120          # Maximum wait (seconds)
```

**Enable Response Detection:**
```yaml
response_detection:
  enabled: true           # Change to true
  check_days: 7
```

**Retry Settings:**
```yaml
retry:
  enabled: true
  max_attempts: 3         # Total retry attempts
```

---

## 📊 What You'll See

### Progress Bar
```
Sending emails: [████████████░░░░░░░░] 60% | 75/125 [01:45<01:10]
```

### Success Messages
```
✓ Sent to: john@example.com
✓ Sent to: jane@startup.io
```

### Failure Messages with Retry
```
WARNING: Attempt 1 failed for invalid@email.com. Retrying in 5s...
WARNING: Attempt 2 failed for invalid@email.com. Retrying in 10s...
✗ Failed to send to invalid@email.com: Invalid email address
```

### Final Statistics
```
============================================================
Campaign Complete!
============================================================
Total sent: 120
Failed: 5
Success rate: 96.0%

Logs saved to: logs/send_email_20241207.log
```

---

## 🔐 Environment Setup

### Set Credentials
```bash
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

### Make Permanent (Linux/Mac)
```bash
echo 'export EMAIL_ADDRESS="your-email@gmail.com"' >> ~/.bashrc
echo 'export EMAIL_PASSWORD="your-app-password"' >> ~/.bashrc
source ~/.bashrc
```

---

## 🤖 Enable Response Detection

### 1. Enable IMAP in Gmail

1. Go to [Gmail Settings](https://mail.google.com/mail/u/0/#settings/fwdandpop)
2. Click **Forwarding and POP/IMAP**
3. Enable **IMAP access**
4. Save changes

### 2. Update Configuration

```bash
nano config.yaml
```

Change:
```yaml
response_detection:
  enabled: true           # Change from false to true
```

### 3. Check Responses

```bash
# Manual check
python check_responses.py

# Or run enhanced scripts (auto-checks before sending)
python send_email_v2.py
```

---

## 📁 File Structure

```
/app/
├── config.yaml                 # ⚙️ Configuration file
├── send_email_v2.py           # 📧 Enhanced email sender
├── send_followup_v2.py        # 📬 Enhanced follow-up sender
├── check_responses.py         # 🔍 Check for replies
├── manage_backups.py          # 💾 Backup manager
├── view_config.py             # 👁️ View configuration
├── backup_manager.py          # Module: Backup system
├── logger_config.py           # Module: Logging system
├── response_detector.py       # Module: Response detection
├── logs/                      # 📊 Log files
│   ├── send_email_20241207.log
│   └── send_followup_20241207.log
├── backups/                   # 💾 Backup folders
│   ├── backup_20241207_103045/
│   └── backup_20241207_153022/
└── [CSV files...]
```

---

## 🎓 Examples

### Example 1: Send Emails with All Features

```bash
# 1. Verify configuration
python view_config.py

# 2. Create manual backup (optional, auto-backup enabled)
python manage_backups.py create

# 3. Check for responses (optional, auto-check enabled)
python check_responses.py

# 4. Send emails with enhanced script
python send_email_v2.py
```

### Example 2: Send Follow-ups

```bash
# Wait 3-5 days after initial emails

# 1. Check who replied
python check_responses.py

# 2. Send follow-ups (skips responders automatically)
python send_followup_v2.py
```

### Example 3: Restore from Backup

```bash
# 1. List available backups
python manage_backups.py list

# 2. Choose backup and restore
python manage_backups.py restore backups/backup_20241207_103045
```

---

## 🐛 Troubleshooting

### Issue: "Environment variables not set"

**Solution:**
```bash
export EMAIL_ADDRESS="your-email@gmail.com"
export EMAIL_PASSWORD="your-app-password"
```

### Issue: Response detection not working

**Solution:**
1. Enable IMAP in Gmail settings
2. Set `response_detection.enabled: true` in config.yaml
3. Verify credentials are correct

### Issue: Progress bar not showing

**Solution:**
Edit config.yaml:
```yaml
progress:
  enabled: true
```

### Issue: Permission denied on scripts

**Solution:**
```bash
chmod +x *.py
```

---

## 📖 Detailed Documentation

- **Full feature guide:** `FEATURES.md`
- **Complete README:** `README.md`
- **Configuration file:** `config.yaml`

---

## 🎯 Pro Tips

1. **Always view config first:**
   ```bash
   python view_config.py
   ```

2. **Use enhanced scripts for better experience:**
   ```bash
   python send_email_v2.py     # Not send_email.py
   ```

3. **Check logs for debugging:**
   ```bash
   tail -f logs/send_email_20241207.log
   ```

4. **Enable response detection to avoid annoying responders:**
   ```yaml
   response_detection:
     enabled: true
   ```

5. **Backups are automatic** - restore if something goes wrong:
   ```bash
   python manage_backups.py list
   python manage_backups.py restore [backup_path]
   ```

---

## ✅ Checklist Before Running

- [ ] Environment variables set (`EMAIL_ADDRESS`, `EMAIL_PASSWORD`)
- [ ] Configuration reviewed (`python view_config.py`)
- [ ] Contacts list ready (`emails.csv`)
- [ ] Resume file present (`resume.pdf`)
- [ ] (Optional) IMAP enabled in Gmail
- [ ] (Optional) Response detection enabled in config

---

## 🚀 Ready to Go!

```bash
# Start sending with all enhanced features
python send_email_v2.py
```

**Happy emailing! 📧**

---

*For detailed feature documentation, see `FEATURES.md`*
