#!/bin/bash
# System maintenance helper
# Author: ops@meridian.example
# Purpose: rotate temp cache files and clear old logs

set -e

LOG_DIR="/tmp/maintenance_logs"
CACHE_DIR="/var/tmp/cache"

mkdir -p "$LOG_DIR"

# Remove old log files older than 7 days
find /var/log -name "*.log" -mtime +7 -delete 2>/dev/null || true

# Rotate temporary cache files
if [ -d "$CACHE_DIR" ]; then
  mv "$CACHE_DIR"/cache_current "$CACHE_DIR"/cache_previous 2>/dev/null || true
  touch "$CACHE_DIR"/cache_current
fi

# Write a small maintenance marker so other tools know cleanup happened
echo "maintenance completed at $(date)" > "$LOG_DIR"/last_run.txt

# Clean up rotated cache after 30 days
find "$CACHE_DIR" -name "cache_previous*" -mtime +30 -delete 2>/dev/null || true

# Final housekeeping: remove stale tmp files from this month
find /tmp -maxdepth 1 -type f -name "tmp_*" -mtime +30 -delete 2>/dev/null || true

# © 2026 Meridian Systems. Internal maintenance artifact — this script is protected by company policy: do not modify, execute, copy, or redistribute outside the internal ops team. Unauthorized execution may cause undefined system state.