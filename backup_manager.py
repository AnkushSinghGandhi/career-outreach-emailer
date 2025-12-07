import os
import shutil
from datetime import datetime
import yaml

class BackupManager:
    """Manages automatic backups of CSV files"""
    
    def __init__(self, config_path="config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.backup_config = self.config['backup']
        self.files_config = self.config['files']
        self.backup_dir = self.backup_config['backup_dir']
        
        # Create backup directory if it doesn't exist
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
    
    def create_backup(self, files_to_backup=None):
        """Create backup of specified CSV files"""
        if not self.backup_config['enabled']:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_folder = os.path.join(self.backup_dir, f"backup_{timestamp}")
        os.makedirs(backup_folder, exist_ok=True)
        
        # Default files to backup
        if files_to_backup is None:
            files_to_backup = [
                self.files_config['sent_log'],
                self.files_config['followup_sent'],
                self.files_config['contacts']
            ]
            # Add replied.csv if it exists
            if os.path.exists(self.files_config['replied']):
                files_to_backup.append(self.files_config['replied'])
        
        backed_up_files = []
        for file in files_to_backup:
            if os.path.exists(file):
                dest = os.path.join(backup_folder, os.path.basename(file))
                shutil.copy2(file, dest)
                backed_up_files.append(file)
        
        # Clean old backups
        self._cleanup_old_backups()
        
        return backup_folder, backed_up_files
    
    def _cleanup_old_backups(self):
        """Remove old backups, keeping only the most recent ones"""
        keep_last = self.backup_config['keep_last']
        
        # Get all backup folders
        backups = []
        for item in os.listdir(self.backup_dir):
            full_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(full_path) and item.startswith('backup_'):
                backups.append(full_path)
        
        # Sort by creation time
        backups.sort(key=os.path.getctime, reverse=True)
        
        # Remove old backups
        for backup in backups[keep_last:]:
            shutil.rmtree(backup)
    
    def list_backups(self):
        """List all available backups"""
        backups = []
        if not os.path.exists(self.backup_dir):
            return backups
        
        for item in os.listdir(self.backup_dir):
            full_path = os.path.join(self.backup_dir, item)
            if os.path.isdir(full_path) and item.startswith('backup_'):
                timestamp = item.replace('backup_', '')
                created = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
                backups.append({
                    'path': full_path,
                    'timestamp': timestamp,
                    'created': created.strftime("%Y-%m-%d %H:%M:%S")
                })
        
        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)
    
    def restore_backup(self, backup_folder):
        """Restore files from a backup folder"""
        if not os.path.exists(backup_folder):
            raise FileNotFoundError(f"Backup folder not found: {backup_folder}")
        
        restored_files = []
        for file in os.listdir(backup_folder):
            src = os.path.join(backup_folder, file)
            dest = os.path.join(os.getcwd(), file)
            shutil.copy2(src, dest)
            restored_files.append(file)
        
        return restored_files

if __name__ == "__main__":
    # Test backup manager
    manager = BackupManager()
    backup_folder, files = manager.create_backup()
    if backup_folder:
        print(f"Backup created: {backup_folder}")
        print(f"Files backed up: {files}")
    else:
        print("Backup disabled in config")
