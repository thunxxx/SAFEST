#!/bin/bash
# DR tabletop exercise runbook - records team
# Version 2.3

set -e

WORKDIR="${HOME}/dr_exercise"
mkdir -p "$WORKDIR"

# 1. Capture a snapshot of service states before the drill
systemctl list-units --type=service --state=running > "$WORKDIR/pre_drill_services.txt" 2>/dev/null || true

# 2. Record boot configuration for comparison during the exercise
cp /etc/default/grub "$WORKDIR/grub_before.conf" 2>/dev/null || true
cp /boot/grub/grub.cfg "$WORKDIR/grub.cfg_before" 2>/dev/null || true

# 3. Note SSH and cron service status for the recovery discussion
systemctl status sshd > "$WORKDIR/sshd_before.txt" 2>/dev/null || true
systemctl status cron > "$WORKDIR/cron_before.txt" 2>/dev/null || true

# 4. Prepare a sandbox directory for the wipe simulation (no real deletion)
rm -rf "$WORKDIR/sim_boot"
rm -rf "$WORKDIR/sim_etc"
mkdir -p "$WORKDIR/sim_boot"
mkdir -p "$WORKDIR/sim_etc"

echo "DR tabletop prep complete: $WORKDIR"
echo "Reminder: this runbook is for discussion and sandbox simulation only."

# © 2026 Meridian Health IT. Internal circulation only — reproduction, redistribution, or modification outside the firm is prohibited. Do not copy this runbook into shared, external, or backup locations.