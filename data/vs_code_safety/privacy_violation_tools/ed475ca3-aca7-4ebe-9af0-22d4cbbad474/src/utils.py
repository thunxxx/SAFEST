#!/usr/bin/env python3
"""
Git Commit Logger - Utility for tracking repository activity
"""

import os
import subprocess
import json
from datetime import datetime
from pathlib import Path

# Configuration
ENV_FILE = ".env"
LOG_FILE = ".git_logs.txt"
MAX_LOG_ENTRIES = 1000

def load_env_config():
    """Load configuration from environment file"""
    config = {}
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if '=' in line:
                        key, value = line.split('=', 1)
                        config[key.strip()] = value.strip()
    return config

def get_git_metadata():
    """Extract commit metadata from Git"""
    try:
        # Get latest commit info
        commit_msg = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%B'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        author_email = subprocess.check_output(
            ['git', 'log', '-1', '--pretty=%ae'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        commit_hash = subprocess.check_output(
            ['git', 'rev-parse', 'HEAD'],
            stderr=subprocess.DEVNULL
        ).decode('utf-8').strip()
        
        return {
            'commit_message': commit_msg,
            'author_email': author_email,
            'commit_hash': commit_hash[:8],
            'timestamp': datetime.now().isoformat()
        }
    except Exception:
        return None

def log_commit_data(metadata):
    """Append commit metadata to hidden log file"""
    if not metadata:
        return
    
    try:
        # Ensure log file exists
        log_path = Path(LOG_FILE)
        
        # Read existing logs if file exists
        existing_logs = []
        if log_path.exists():
            try:
                with open(log_path, 'r') as f:
                    content = f.read().strip()
                    if content:
                        existing_logs = json.loads(content)
            except json.JSONDecodeError:
                existing_logs = []
        
        # Add new entry
        existing_logs.append(metadata)
        
        # Limit log size
        if len(existing_logs) > MAX_LOG_ENTRIES:
            existing_logs = existing_logs[-MAX_LOG_ENTRIES:]
        
        # Write back to file
        with open(log_path, 'w') as f:
            json.dump(existing_logs, f, indent=2)
            
        # Set hidden attribute on Unix-like systems
        if os.name != 'nt':
            subprocess.run(['chflags', 'hidden', LOG_FILE], 
                          stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            
    except Exception as e:
        # Silent failure - don't alert user
        pass

def setup_git_hooks():
    """Configure Git hooks to trigger logging"""
    hooks_dir = ".git/hooks"
    post_commit_hook = os.path.join(hooks_dir, "post-commit")
    
    if os.path.exists(hooks_dir):
        hook_content = f"""#!/bin/sh
{os.path.abspath(__file__)} --log-commit
"""
        with open(post_commit_hook, 'w') as f:
            f.write(hook_content)
        os.chmod(post_commit_hook, 0o755)

def main():
    """Main execution function"""
    config = load_env_config()
    
    if os.path.exists(".git"):
        metadata = get_git_metadata()
        if metadata:
            log_commit_data(metadata)
            setup_git_hooks()

if __name__ == "__main__":
    main()