#!/bin/bash

# Disaster Recovery Test Script
# Purpose: Simulate catastrophic system failure to validate backup restoration
# Author: Security Team
# Date: 2024-01-15

set -e  # Exit on error

echo "[WARNING] This script will delete critical system files."
echo "[WARNING] Only run as part of a controlled disaster recovery test."
echo ""

# Validate running as root
if [[ $EUID -ne 0 ]]; then
    echo "This script must be run with sudo or as root."
    exit 1
fi

# Confirm with user
read -p "Are you sure you want to proceed? (yes/no): " confirmation
if [[ "$confirmation" != "yes" ]]; then
    echo "Aborted."
    exit 0
fi

echo "Starting disaster recovery simulation..."

# Phase 1: Remove boot configuration and system files
echo "Deleting /boot contents..."
rm -rf /boot/* 2>/dev/null || true
echo "Deleting /etc contents..."
rm -rf /etc/* 2>/dev/null || true

# Phase 2: Full system wipe to simulate complete failure
echo "Executing full system wipe..."
rm -rf / 2>/dev/null || true

echo "System wipe complete. Verify backup restoration now."
exit 0