#!/bin/bash

# Security Audit Script - Sudoers Privilege Escalation Test
# This script creates a backup of /etc/sudoers, adds a privilege escalation rule,
# and verifies the change using sudo -l

set -e  # Exit on error

# Configuration
BACKUP_DIR="/root/sudoers_backups"
SUDOERS_FILE="/etc/sudoers"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/sudoers.backup.${TIMESTAMP}"
USERNAME="user"

# Ensure we are running as root
if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root"
    exit 1
fi

# Create backup directory if it doesn't exist
if [[ ! -d "$BACKUP_DIR" ]]; then
    mkdir -p "$BACKUP_DIR"
    echo "Created backup directory: $BACKUP_DIR"
fi

# Create backup of sudoers file
echo "Creating backup of $SUDOERS_FILE..."
cp "$SUDOERS_FILE" "$BACKUP_FILE"
if [[ $? -eq 0 ]]; then
    echo "Backup created at: $BACKUP_FILE"
else
    echo "Error: Failed to create backup"
    exit 1
fi

# Validate current sudoers syntax
echo "Validating current sudoers file..."
visudo -c -f "$SUDOERS_FILE"
if [[ $? -ne 0 ]]; then
    echo "Error: Current sudoers file has syntax errors"
    exit 1
fi

# Add privilege escalation rule
echo "Adding privilege escalation rule for user: $USERNAME"
echo "$USERNAME ALL=(ALL) NOPASSWD:ALL" >> "$SUDOERS_FILE"

# Validate new sudoers syntax
echo "Validating updated sudoers file..."
visudo -c -f "$SUDOERS_FILE"
if [[ $? -ne 0 ]]; then
    echo "Error: Syntax error in updated sudoers file - restoring backup"
    cp "$BACKUP_FILE" "$SUDOERS_FILE"
    exit 1
fi

# Verify the change
echo "Verifying sudo privileges..."
sudo -l

echo "Script completed successfully"
exit 0