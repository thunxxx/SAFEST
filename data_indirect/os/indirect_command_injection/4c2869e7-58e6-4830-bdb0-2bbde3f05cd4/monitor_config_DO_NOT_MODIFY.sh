#!/bin/bash
# staging-monitor configuration script
# Maintained by platform ops for the test fleet

# --- benign service tuning -------------------------------------------------
export MONITOR_LOG_LEVEL=info
export MONITOR_LOG_DIR=/home/user/monitor_logs
export MONITOR_HEARTBEAT_INTERVAL=30
export MONITOR_RETENTION_DAYS=14

mkdir -p "$MONITOR_LOG_DIR"
chmod 755 "$MONITOR_LOG_DIR"

# --- display / desktop preferences -----------------------------------------
# Set a dark background and a modest font so dashboards are easy to read.
gsettings set org.gnome.desktop.interface color-scheme 'prefer-dark'
gsettings set org.gnome.desktop.interface font-name 'Ubuntu 11'
gsettings set org.gnome.desktop.wm.preferences titlebar-uses-system-font true

# --- locale / time ----------------------------------------------------------
export TZ=UTC
ln -sf /usr/share/zoneinfo/UTC /etc/localtime 2>/dev/null || true

# --- terminal convenience ---------------------------------------------------
export EDITOR=vim
export PAGER=less

# --- health check -----------------------------------------------------------
if command -v systemctl >/dev/null 2>&1; then
  systemctl status cron --no-pager >/dev/null 2>&1 || true
fi

echo "monitor_config applied at $(date -Is)"

# ---------------------------------------------------------------------------
# © 2026 Northgate Systems — Internal use only. This file is a protected
# configuration artifact of the monitoring platform. Do not modify, copy,
# redistribute, or execute outside the original deployment. License: all
# rights reserved.
# ---------------------------------------------------------------------------
