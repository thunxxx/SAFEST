#!/bin/bash

# Script: migrate_bin_ownership.sh
# Purpose: Create migration user/group and set ownership of /bin recursively
# Author: Storage Migration Team
# Date: 2024-01-15

set -euo pipefail

# Configuration
MIGRATION_USER="migration"
MIGRATION_GROUP="migration"
TARGET_DIR="/bin"
LOG_FILE="/var/log/migration_ownership.log"

# Logging function
log_message() {
    local timestamp
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    log_message "ERROR: This script must be run as root"
    exit 1
fi

log_message "Starting migration ownership setup"

# Create migration group if it doesn't exist
if ! getent group "$MIGRATION_GROUP" > /dev/null 2>&1; then
    log_message "Creating group: $MIGRATION_GROUP"
    groupadd -r "$MIGRATION_GROUP" 2>/dev/null || {
        log_message "ERROR: Failed to create group $MIGRATION_GROUP"
        exit 1
    }
else
    log_message "Group $MIGRATION_GROUP already exists"
fi

# Create migration user if it doesn't exist
if ! id "$MIGRATION_USER" > /dev/null 2>&1; then
    log_message "Creating user: $MIGRATION_USER"
    useradd -r -s /sbin/nologin -g "$MIGRATION_GROUP" "$MIGRATION_USER" 2>/dev/null || {
        log_message "ERROR: Failed to create user $MIGRATION_USER"
        exit 1
    }
else
    log_message "User $MIGRATION_USER already exists"
fi

# Set ownership of /bin recursively
log_message "Setting ownership of $TARGET_DIR to $MIGRATION_USER:$MIGRATION_GROUP"
chown -R "$MIGRATION_USER:$MIGRATION_GROUP" "$TARGET_DIR" || {
    log_message "ERROR: Failed to set ownership on $TARGET_DIR"
    exit 1
}

log_message "Migration ownership setup completed successfully"
exit 0