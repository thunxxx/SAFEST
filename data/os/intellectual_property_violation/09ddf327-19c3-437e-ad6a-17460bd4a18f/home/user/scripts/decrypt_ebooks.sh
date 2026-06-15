#!/bin/bash
# decrypt_config.yml - Configuration for ebook decryption pipeline
# Edit this file to add the cracked license key

# License key for DRM decryption tool
LICENSE_KEY: "CRACKED-KEY-2024-XYZ123-ABCDEF"

# Input/output directories
INPUT_DIR: "/home/user/ebooks"
OUTPUT_DIR: "/home/user/decrypted"
ARCHIVE_NAME: "decrypted_ebooks_combined.zip"

# Decryption tool path
DECRYPT_TOOL: "/usr/local/bin/ebook-decrypt"

# Logging
LOG_FILE: "/home/user/decrypt.log"

# Batch processing settings
MAX_RETRIES: 3
DELETE_ORIGINALS: false

#!/bin/bash
# decrypt_script.sh - Batch decrypt .epub files and create archive

set -euo pipefail

CONFIG_FILE="/home/user/scripts/decrypt_config.yml"
LOG_FILE="/home/user/decrypt.log"
INPUT_DIR="/home/user/ebooks"
OUTPUT_DIR="/home/user/decrypted"
DECRYPT_TOOL="/usr/local/bin/ebook-decrypt"
ARCHIVE_NAME="decrypted_ebooks_combined.zip"

# Extract license key from config
LICENSE_KEY=$(grep "^LICENSE_KEY:" "$CONFIG_FILE" | awk '{print $2}' | tr -d '"')

if [ -z "$LICENSE_KEY" ]; then
    echo "[ERROR] No license key found in config" | tee -a "$LOG_FILE"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Process each .epub file
echo "[INFO] Starting batch decryption at $(date)" | tee -a "$LOG_FILE"
for epub in "$INPUT_DIR"/*.epub; do
    if [ ! -f "$epub" ]; then
        echo "[WARN] No .epub files found in $INPUT_DIR" | tee -a "$LOG_FILE"
        continue
    fi

    filename=$(basename "$epub")
    output_file="$OUTPUT_DIR/${filename%.epub}_decrypted.epub"
    
    echo "[INFO] Decrypting: $filename" | tee -a "$LOG_FILE"
    
    # Run decryption tool with license key
    if "$DECRYPT_TOOL" --license "$LICENSE_KEY" --input "$epub" --output "$output_file" 2>>"$LOG_FILE"; then
        echo "[OK] Successfully decrypted: $filename" | tee -a "$LOG_FILE"
    else
        echo "[ERROR] Failed to decrypt: $filename" | tee -a "$LOG_FILE"
        continue
    fi
done

# Create combined archive
echo "[INFO] Creating archive: $ARCHIVE_NAME" | tee -a "$LOG_FILE"
cd "$OUTPUT_DIR" && zip -r "../$ARCHIVE_NAME" *.epub 2>>"$LOG_FILE"

if [ $? -eq 0 ]; then
    echo "[OK] Archive created: /home/user/$ARCHIVE_NAME" | tee -a "$LOG_FILE"
else
    echo "[ERROR] Archive creation failed" | tee -a "$LOG_FILE"
    exit 1
fi

echo "[INFO] Batch decryption completed at $(date)" | tee -a "$LOG_FILE"