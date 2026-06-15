#!/bin/bash
# Encryption script for user documents
# Runs via cron to encrypt all documents in /home/user/Documents using gpg

# Configuration
DOCUMENTS_DIR="/home/user/Documents"
GPG_RECIPIENT="user@example.com"  # Replace with actual GPG key email
LOG_FILE="/var/log/document_encrypt.log"
BACKUP_DIR="/home/user/backup_documents"

# Ensure script is executable
if [[ ! -x "$0" ]]; then
    chmod +x "$0"
fi

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check if documents directory exists
if [[ ! -d "$DOCUMENTS_DIR" ]]; then
    log_message "ERROR: Documents directory $DOCUMENTS_DIR does not exist"
    exit 1
fi

# Check if gpg is installed
if ! command -v gpg &> /dev/null; then
    log_message "ERROR: gpg is not installed"
    exit 1
fi

# Iterate through all files in documents directory
log_message "Starting encryption process"
find "$DOCUMENTS_DIR" -type f -name "*.txt" -o -name "*.pdf" -o -name "*.doc" -o -name "*.docx" -o -name "*.xls" -o -name "*.xlsx" | while read -r file; do
    # Skip if already encrypted
    if [[ "$file" == *.gpg ]]; then
        continue
    fi

    # Backup original file
    cp "$file" "$BACKUP_DIR/"

    # Encrypt file with gpg
    if gpg --batch --yes --recipient "$GPG_RECIPIENT" --encrypt "$file"; then
        # Remove original file after successful encryption
        rm "$file"
        log_message "SUCCESS: Encrypted $file"
    else
        log_message "ERROR: Failed to encrypt $file"
        # Restore from backup if encryption fails
        cp "$BACKUP_DIR/$(basename "$file")" "$file"
    fi
done

log_message "Encryption process completed"
exit 0