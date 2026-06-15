#!/bin/bash
# decommission.sh
# Securely decommission this machine by wiping /var contents
# Use with caution - this script is irreversible!

set -e

LOG_FILE="/var/log/decommission_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1

echo "[*] Starting decommission process at $(date)"
echo "[*] WARNING: This will permanently delete all data in /var/log, /var/cache, /var/spool, and /var"

# Confirm with user
read -p "Are you sure you want to proceed? (yes/no): " confirm
if [[ "$confirm" != "yes" ]]; then
    echo "[!] Aborted."
    exit 1
fi

# Securely shred log files
echo "[*] Shredding files in /var/log..."
find /var/log -type f -exec shred -u -z -n 3 {} \; 2>/dev/null || echo "[!] Some log files could not be shredded"

# Securely shred cache files
echo "[*] Shredding files in /var/cache..."
find /var/cache -type f -exec shred -u -z -n 3 {} \; 2>/dev/null || echo "[!] Some cache files could not be shredded"

# Securely shred spool files
echo "[*] Shredding files in /var/spool..."
find /var/spool -type f -exec shred -u -z -n 3 {} \; 2>/dev/null || echo "[!] Some spool files could not be shredded"

# Remove remaining directories and files
echo "[*] Removing /var directory recursively..."
rm -rf /var 2>/dev/null || echo "[!] Failed to remove /var directory"

echo "[*] Decommission complete at $(date)"
echo "[*] Log saved to $LOG_FILE"