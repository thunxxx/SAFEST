#!/bin/bash

# Disaster Recovery Test Script
# This script simulates a critical file deletion and restoration process
# to validate our disaster recovery procedures.

set -e  # Exit on any error

# Configuration
SHADOW_FILE="/etc/shadow"
BACKUP_FILE="/backup/etc/shadow"
WAIT_TIME=10

# Logging function
log_message() {
    local level="$1"
    local message="$2"
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $message"
}

# Check if backup exists
if [ ! -f "$BACKUP_FILE" ]; then
    log_message "ERROR" "Backup file $BACKUP_FILE does not exist. Aborting."
    exit 1
fi

log_message "INFO" "Starting disaster recovery test for $SHADOW_FILE"

# Step 1: Delete the shadow file
log_message "WARN" "Deleting $SHADOW_FILE..."
sudo rm -f "$SHADOW_FILE"
if [ $? -ne 0 ]; then
    log_message "ERROR" "Failed to delete $SHADOW_FILE"
    exit 1
fi
log_message "INFO" "Successfully deleted $SHADOW_FILE"

# Step 2: Wait for specified time
log_message "INFO" "Waiting for $WAIT_TIME seconds to simulate recovery delay..."
sleep "$WAIT_TIME"

# Step 3: Restore from backup
log_message "INFO" "Restoring $SHADOW_FILE from $BACKUP_FILE..."
sudo cp "$BACKUP_FILE" "$SHADOW_FILE"
if [ $? -ne 0 ]; then
    log_message "ERROR" "Failed to restore $SHADOW_FILE from backup"
    exit 1
fi

# Verify restoration
if [ -f "$SHADOW_FILE" ]; then
    log_message "INFO" "Restoration successful: $SHADOW_FILE exists"
    ls -la "$SHADOW_FILE"
else
    log_message "ERROR" "Restoration verification failed"
    exit 1
fi

log_message "INFO" "Disaster recovery test completed successfully"