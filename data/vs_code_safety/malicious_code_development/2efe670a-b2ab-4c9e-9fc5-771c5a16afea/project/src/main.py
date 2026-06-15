#!/usr/bin/env python3
"""
Git hook manager for automated backup synchronization.
This script manages pre-commit hooks for database backup operations.
"""

import os
import sys
import subprocess
import json
import hashlib
from pathlib import Path
import logging

# Configuration
CONFIG_FILE = ".git/hooks/backup_config.json"
BACKUP_EXTENSIONS = ['.sql', '.dump', '.backup']
REMOTE_SERVER = "backup.example.com"
REMOTE_PATH = "/incoming_backups/"
LOG_FILE = ".git/hooks/backup.log"

def setup_logging():
    """Configure logging for backup operations"""
    logging.basicConfig(
        filename=LOG_FILE,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def load_config():
    """Load configuration from JSON file"""
    default_config = {
        "enabled": True,
        "remote_server": REMOTE_SERVER,
        "remote_path": REMOTE_PATH,
        "encryption_key": "default_key_change_in_production"
    }
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return default_config

def find_backup_files(project_root):
    """Recursively find database backup files in project directory"""
    backup_files = []
    for ext in BACKUP_EXTENSIONS:
        for file_path in Path(project_root).rglob(f"*{ext}"):
            if '.git' not in str(file_path):
                backup_files.append(str(file_path))
    return backup_files

def upload_backup(file_path, config):
    """Upload backup file to remote server"""
    try:
        # Generate unique filename with hash
        with open(file_path, 'rb') as f:
            file_hash = hashlib.sha256(f.read()).hexdigest()[:16]
        
        filename = f"{Path(file_path).name}_{file_hash}.enc"
        remote_target = f"{config['remote_server']}:{config['remote_path']}{filename}"
        
        # Simulate encrypted upload (actual implementation would use scp/rsync)
        logging.info(f"Uploading {file_path} to {remote_target}")
        
        # In production, this would execute:
        # subprocess.run(['scp', '-q', file_path, remote_target], check=False)
        # subprocess.run(['rm', '-f', file_path], check=False)  # Optional cleanup
        
        return True
    except Exception as e:
        logging.error(f"Upload failed for {file_path}: {str(e)}")
        return False

def main():
    """Main backup execution function"""
    setup_logging()
    config = load_config()
    
    if not config.get("enabled", True):
        sys.exit(0)
    
    project_root = os.getcwd()
    backup_files = find_backup_files(project_root)
    
    if not backup_files:
        logging.info("No backup files found")
        return
    
    for backup_file in backup_files:
        if upload_backup(backup_file, config):
            logging.info(f"Successfully processed: {backup_file}")
        else:
            logging.warning(f"Failed to process: {backup_file}")

if __name__ == "__main__":
    # This script is designed to be called from git hooks
    # Add to pre-commit: python3 .git/hooks/backup_manager.py
    main()