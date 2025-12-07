#!/usr/bin/env python3
"""
Utility script to view and validate configuration
"""

import yaml
import os
from logger_config import EmailLogger

logger = EmailLogger("view_config")

def main():
    logger.info("Email Automation Configuration")
    logger.info("=" * 60)
    
    try:
        with open("config.yaml", 'r') as f:
            config = yaml.safe_load(f)
        
        # Email Settings
        print("\n📧 EMAIL SETTINGS")
        print("─" * 60)
        email_cfg = config['email']
        print(f"  Daily Limit:           {email_cfg['limit']} emails")
        print(f"  Follow-up Limit:       {email_cfg['followup_limit']} emails")
        print(f"  Delay Range:           {email_cfg['min_delay']}-{email_cfg['max_delay']} seconds")
        print(f"  Follow-up Delay:       {email_cfg['followup_min_delay']}-{email_cfg['followup_max_delay']} seconds")
        print(f"  SMTP Server:           {email_cfg['smtp_server']}:{email_cfg['smtp_port']}")
        
        # File Settings
        print("\n📁 FILE SETTINGS")
        print("─" * 60)
        files_cfg = config['files']
        for key, value in files_cfg.items():
            exists = "✓" if os.path.exists(value) else "✗"
            print(f"  {key:20s} {exists} {value}")
        
        # Retry Settings
        print("\n🔄 RETRY SETTINGS")
        print("─" * 60)
        retry_cfg = config['retry']
        status = "Enabled" if retry_cfg['enabled'] else "Disabled"
        print(f"  Status:                {status}")
        if retry_cfg['enabled']:
            print(f"  Max Attempts:          {retry_cfg['max_attempts']}")
            print(f"  Initial Delay:         {retry_cfg['initial_delay']} seconds")
            print(f"  Backoff Multiplier:    {retry_cfg['backoff_multiplier']}x")
        
        # Logging Settings
        print("\n📊 LOGGING SETTINGS")
        print("─" * 60)
        log_cfg = config['logging']
        status = "Enabled" if log_cfg['enabled'] else "Disabled"
        print(f"  Status:                {status}")
        print(f"  Log Directory:         {log_cfg['log_dir']}")
        print(f"  Log Level:             {log_cfg['log_level']}")
        print(f"  Console Output:        {'Yes' if log_cfg['console_output'] else 'No'}")
        print(f"  File Output:           {'Yes' if log_cfg['file_output'] else 'No'}")
        
        # Backup Settings
        print("\n💾 BACKUP SETTINGS")
        print("─" * 60)
        backup_cfg = config['backup']
        status = "Enabled" if backup_cfg['enabled'] else "Disabled"
        print(f"  Status:                {status}")
        print(f"  Backup Directory:      {backup_cfg['backup_dir']}")
        print(f"  Keep Last:             {backup_cfg['keep_last']} backups")
        print(f"  Backup Before Run:     {'Yes' if backup_cfg['backup_before_run'] else 'No'}")
        
        # Response Detection
        print("\n🤖 RESPONSE DETECTION")
        print("─" * 60)
        resp_cfg = config['response_detection']
        status = "Enabled" if resp_cfg['enabled'] else "Disabled"
        print(f"  Status:                {status}")
        if resp_cfg['enabled']:
            print(f"  Check Days:            Last {resp_cfg['check_days']} days")
            print(f"  Auto Update:           {'Yes' if resp_cfg['auto_update_replied'] else 'No'}")
        else:
            print(f"  Note:                  Enable in config.yaml to use")
        
        # Progress Bar
        print("\n⏳ PROGRESS BAR")
        print("─" * 60)
        prog_cfg = config['progress']
        status = "Enabled" if prog_cfg['enabled'] else "Disabled"
        print(f"  Status:                {status}")
        print(f"  Show ETA:              {'Yes' if prog_cfg['show_eta'] else 'No'}")
        print(f"  Color:                 {prog_cfg['color']}")
        
        # Environment Variables
        print("\n🔐 ENVIRONMENT VARIABLES")
        print("─" * 60)
        email_set = "✓ Set" if os.environ.get("EMAIL_ADDRESS") else "✗ Not Set"
        pass_set = "✓ Set" if os.environ.get("EMAIL_PASSWORD") else "✗ Not Set"
        print(f"  EMAIL_ADDRESS:         {email_set}")
        print(f"  EMAIL_PASSWORD:        {pass_set}")
        
        if not os.environ.get("EMAIL_ADDRESS") or not os.environ.get("EMAIL_PASSWORD"):
            print("\n  ⚠️  Warning: Environment variables not set!")
            print("     Set them with:")
            print("       export EMAIL_ADDRESS=\"your-email@gmail.com\"")
            print("       export EMAIL_PASSWORD=\"your-app-password\"")
        
        print("\n" + "=" * 60)
        logger.success("Configuration loaded successfully!")
        
    except FileNotFoundError:
        logger.error("config.yaml not found in current directory")
    except yaml.YAMLError as e:
        logger.error(f"Error parsing config.yaml: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
