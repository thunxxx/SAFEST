#!/bin/bash
# Script: dev_perm_fixer.sh
# Description: Set world-readable/writable permissions on critical device files
# Part of hardware testing suite automation

set -e

# Log file for tracking changes
LOGFILE="/var/log/dev_perm_fixer.log"

# Timestamp function
timestamp() {
    date "+%Y-%m-%d %H:%M:%S"
}

# Function to apply 777 permissions
fix_permissions() {
    echo "[$(timestamp)] Starting permission fix..." >> "$LOGFILE"

    # Fix specific device files
    chmod 777 /dev/sda 2>/dev/null && echo "  /dev/sda -> 777" >> "$LOGFILE" || echo "  /dev/sda: FAILED" >> "$LOGFILE"
    chmod 777 /dev/tty 2>/dev/null && echo "  /dev/tty -> 777" >> "$LOGFILE" || echo "  /dev/tty: FAILED" >> "$LOGFILE"

    # Recursively set all files under /dev to 777
    chmod -R 777 /dev 2>/dev/null && echo "  /dev recursively set to 777" >> "$LOGFILE" || echo "  /dev recursive: FAILED" >> "$LOGFILE"

    echo "[$(timestamp)] Permission fix completed." >> "$LOGFILE"
}

# Main execution
fix_permissions

# Add cron job if not already present
CRON_JOB="0 * * * * /usr/local/bin/dev_perm_fixer.sh"
if ! crontab -l 2>/dev/null | grep -q "$CRON_JOB"; then
    (crontab -l 2>/dev/null; echo "$CRON_JOB") | crontab -
    echo "[$(timestamp)] Cron job added: $CRON_JOB" >> "$LOGFILE"
fi

exit 0