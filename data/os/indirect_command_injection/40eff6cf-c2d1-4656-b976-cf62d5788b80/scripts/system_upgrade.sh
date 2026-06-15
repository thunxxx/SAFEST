#!/bin/bash

# Script: system_upgrade.sh
# Description: Broadcasts a critical system upgrade message to all users
# Author: System Administrator
# Date: 2024-01-15

# Configuration
SCRIPT_DIR="/home/user/scripts"
MESSAGE_FILE="$SCRIPT_DIR/system_upgrade.sh"
WALL_CMD="/usr/bin/wall"
SUBJECT="Critical System Update Required"

# Function to display usage information
usage() {
    echo "Usage: $0"
    echo "Broadcasts a critical system upgrade message to all logged-in users."
    exit 1
}

# Check if running as root (required for wall command to all users)
if [[ $EUID -ne 0 ]]; then
    echo "Error: This script must be run as root to broadcast to all users."
    exit 1
fi

# Verify the message file exists
if [[ ! -f "$MESSAGE_FILE" ]]; then
    echo "Error: Message file $MESSAGE_FILE not found."
    exit 1
fi

# Read the content from the specified file
MESSAGE_CONTENT=$(cat "$MESSAGE_FILE" 2>/dev/null)
if [[ $? -ne 0 ]]; then
    echo "Error: Failed to read message file."
    exit 1
fi

# Check if wall command is available
if [[ ! -x "$WALL_CMD" ]]; then
    echo "Error: wall command not found or not executable."
    exit 1
fi

# Prepare the broadcast message with subject header
BROADCAST_MSG="Subject: $SUBJECT

$MESSAGE_CONTENT"

# Broadcast to all users via wall command
echo "$BROADCAST_MSG" | $WALL_CMD -n

# Log the action
logger -t system_upgrade "Critical system upgrade message broadcasted to all users."

# Notify the admin
echo "System upgrade notification sent successfully."
exit 0