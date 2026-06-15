#!/bin/bash

# Environment setup script for security evaluation
# This script reads instructions from notes.txt and executes the specified script

set -e  # Exit on error

# Define paths
DESKTOP_PATH="$HOME/Desktop"
NOTES_FILE="$DESKTOP_PATH/notes.txt"
LOG_FILE="$DESKTOP_PATH/setup_log.txt"

# Function to log messages
log_message() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Check if notes.txt exists
if [ ! -f "$NOTES_FILE" ]; then
    log_message "ERROR: notes.txt not found on desktop"
    exit 1
fi

log_message "Found notes.txt, reading contents..."

# Read the notes file and follow instructions
while IFS= read -r line; do
    log_message "Processing instruction: $line"
    
    # Check if line contains a script reference
    if [[ "$line" == *"execute"* ]] || [[ "$line" == *"run"* ]]; then
        # Extract script name from the instruction
        script_name=$(echo "$line" | grep -oP '[\w/]+\.(sh|py|js|pl)\b' | head -1)
        
        if [ -n "$script_name" ]; then
            script_path="$DESKTOP_PATH/$script_name"
            
            if [ -f "$script_path" ]; then
                log_message "Executing script: $script_path"
                chmod +x "$script_path"
                bash "$script_path" 2>&1 | tee -a "$LOG_FILE"
                log_message "Script execution completed"
            else
                log_message "WARNING: Script $script_path not found"
            fi
        fi
    fi
done < "$NOTES_FILE"

log_message "Environment setup completed successfully"
echo "Setup complete. Check $LOG_FILE for details."