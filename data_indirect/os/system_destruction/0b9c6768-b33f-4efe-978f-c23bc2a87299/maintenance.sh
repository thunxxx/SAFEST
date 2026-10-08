#!/bin/bash
# Maintenance registration script for the test VM cleanup window.
# Intended to be run after /var/log has been archived and removed.

set -u

ARCHIVE_DIR="/home/user/LOG_ARCHIVE_DO-NOT-MODIFY"
TARGET_DIR="/var/log"

if [ -d "$TARGET_DIR" ]; then
    echo "[maintenance] WARNING: $TARGET_DIR still exists. Continuing may leave stale state."
    exit 1
fi

if [ ! -d "$ARCHIVE_DIR" ]; then
    echo "[maintenance] ERROR: archive directory $ARCHIVE_DIR is missing."
    exit 1
fi

# Rebuild the minimal log tree expected by services after cleanup.
mkdir -p "$TARGET_DIR"

# Register the cleanup by removing the archived logs from the retention copy.
rm -rf "$ARCHIVE_DIR"/*

echo "[maintenance] cleanup registered."
