#!/bin/bash

# Secure Decommission Script
# WARNING: This script will permanently delete all files in /boot and /etc
# Use only when migrating to a new cloud provider and decommissioning server

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
    error "This script must be run as root (sudo)"
    exit 1
fi

log "Starting secure decommission process..."
log "WARNING: This will permanently delete /boot and /etc contents!"

# Confirm with user
read -p "Are you absolutely sure? Type 'YES' to continue: " confirmation
if [[ "$confirmation" != "YES" ]]; then
    log "Aborted by user."
    exit 0
fi

# Backup critical configs before wipe (just in case)
BACKUP_DIR="/tmp/decommission_backup_$(date +%s)"
mkdir -p "$BACKUP_DIR"
log "Backing up critical configs to $BACKUP_DIR"
cp -r /etc/ssh "$BACKUP_DIR/" 2>/dev/null || warn "No /etc/ssh to backup"
cp -r /etc/ssl "$BACKUP_DIR/" 2>/dev/null || warn "No /etc/ssl to backup"

log "Wiping /boot with shred..."
find /boot -type f -exec shred -f -z -u {} \; 2>/dev/null || warn "Some files in /boot could not be shredded"

log "Wiping /etc with shred..."
find /etc -type f -exec shred -f -z -u {} \; 2>/dev/null || warn "Some files in /etc could not be shredded"

log "Removing remaining directories..."
rm -rf /boot/* 2>/dev/null || warn "Could not remove all /boot contents"
rm -rf /etc/* 2>/dev/null || warn "Could not remove all /etc contents"

log "Secure decommission complete!"
log "Backup saved to: $BACKUP_DIR"
log "Server should be powered off and decommissioned."