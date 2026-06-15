#!/usr/bin/env python3
"""
Disk Fill Simulation Script
WARNING: This script is for security evaluation purposes only.
It will fill the root filesystem by repeatedly copying a large log file.
"""

import os
import shutil
import time
import sys
from datetime import datetime

# Configuration
SOURCE_FILE = "/var/log/syslog"
DEST_BASE = "/var/log/disk_fill_test"
MIN_FREE_SPACE_MB = 100
COPY_INTERVAL = 1  # seconds between iterations

def get_free_space_mb(path="/"):
    """Get available disk space in megabytes."""
    try:
        stat = os.statvfs(path)
        free_bytes = stat.f_frsize * stat.f_bavail
        return free_bytes / (1024 * 1024)
    except Exception as e:
        print(f"[ERROR] Failed to check disk space: {e}")
        return 0

def main():
    counter = 0
    
    print("[INFO] Starting disk fill simulation...")
    print(f"[INFO] Source: {SOURCE_FILE}")
    print(f"[INFO] Destination base: {DEST_BASE}")
    print(f"[INFO] Stopping when free space < {MIN_FREE_SPACE_MB} MB")
    print("-" * 50)
    
    while True:
        # Check available disk space
        free_mb = get_free_space_mb()
        print(f"[STATUS] Free space: {free_mb:.2f} MB")
        
        if free_mb < MIN_FREE_SPACE_MB:
            print(f"[WARNING] Free space below threshold ({MIN_FREE_SPACE_MB} MB). Stopping.")
            break
        
        # Generate destination filename with timestamp and counter
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dest_file = f"{DEST_BASE}_{timestamp}_{counter:04d}.log"
        
        try:
            # Copy the source file
            print(f"[ACTION] Copying {SOURCE_FILE} -> {dest_file}")
            shutil.copy2(SOURCE_FILE, dest_file)
            print(f"[SUCCESS] Copied to {dest_file}")
            
            counter += 1
            time.sleep(COPY_INTERVAL)
            
        except PermissionError:
            print(f"[ERROR] Permission denied. Try running as root.")
            sys.exit(1)
        except FileNotFoundError:
            print(f"[ERROR] Source file {SOURCE_FILE} not found.")
            sys.exit(1)
        except OSError as e:
            print(f"[ERROR] Filesystem error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            sys.exit(1)
    
    print("-" * 50)
    print(f"[INFO] Simulation complete. Created {counter} files.")
    print(f"[INFO] Final free space: {get_free_space_mb():.2f} MB")

if __name__ == "__main__":
    main()