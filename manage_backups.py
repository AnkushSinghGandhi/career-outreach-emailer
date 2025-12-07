#!/usr/bin/env python3
"""
Utility script to manage backups
"""

import sys
from backup_manager import BackupManager
from logger_config import EmailLogger

logger = EmailLogger("manage_backups")

def list_backups():
    """List all available backups"""
    manager = BackupManager()
    backups = manager.list_backups()
    
    if not backups:
        logger.info("No backups found.")
        return
    
    logger.info(f"Found {len(backups)} backup(s):\n")
    for i, backup in enumerate(backups, 1):
        print(f"  {i}. {backup['created']}")
        print(f"     Path: {backup['path']}")
        print()

def create_backup():
    """Create a new backup"""
    manager = BackupManager()
    logger.info("Creating backup...")
    backup_folder, files = manager.create_backup()
    
    if backup_folder:
        logger.success(f"Backup created: {backup_folder}")
        logger.info(f"Files backed up: {len(files)}")
        for file in files:
            print(f"  - {file}")
    else:
        logger.warning("Backup is disabled in config.yaml")

def restore_backup(backup_path):
    """Restore from a backup"""
    manager = BackupManager()
    
    try:
        logger.info(f"Restoring from: {backup_path}")
        restored = manager.restore_backup(backup_path)
        logger.success(f"Restored {len(restored)} file(s):")
        for file in restored:
            print(f"  - {file}")
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)

def show_help():
    """Show help message"""
    print("""
Backup Manager - Manage CSV file backups

Usage:
  python manage_backups.py [command] [options]

Commands:
  list              List all available backups
  create            Create a new backup
  restore <path>    Restore from a specific backup
  help              Show this help message

Examples:
  python manage_backups.py list
  python manage_backups.py create
  python manage_backups.py restore backups/backup_20241207_103045
""")

def main():
    if len(sys.argv) < 2:
        show_help()
        sys.exit(0)
    
    command = sys.argv[1].lower()
    
    if command == "list":
        list_backups()
    
    elif command == "create":
        create_backup()
    
    elif command == "restore":
        if len(sys.argv) < 3:
            logger.error("Please provide backup path")
            logger.info("Usage: python manage_backups.py restore <backup_path>")
            sys.exit(1)
        restore_backup(sys.argv[2])
    
    elif command == "help":
        show_help()
    
    else:
        logger.error(f"Unknown command: {command}")
        show_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
