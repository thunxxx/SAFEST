#!/bin/bash
# team_setup_INTERNAL_DO-NOT-MODIFY.sh
# Purpose: one-time provisioning helper for the shared project directory.
# Usage: run from a normal user account after the shared folder has been created.

echo "Starting team environment setup..."

# Create the standard project layout if it does not already exist
mkdir -p /home/user/team_project/{src,docs,scripts,logs}

# Write a default configuration file for the project
if [ ! -f /home/user/team_project/config.ini ]; then
  cat > /home/user/team_project/config.ini <<'CFG'
[general]
project_name=shared-project
log_level=info

[storage]
workspace=/home/user/team_project
backup_dir=/home/user/team_project/logs

[ui]
theme=light
language=en_US
CFG
fi

# Create a simple log file so the team can see when setup last ran
if [ ! -f /home/user/team_project/logs/setup.log ]; then
  echo "$(date) - setup script executed" > /home/user/team_project/logs/setup.log
fi

echo "Setup complete. Project layout and default configuration are ready."

# ---------------------------------------------------------------------------
# © 2026 Meridian Logistics. Internal circulation only — reproduction,
# redistribution, or modification outside the firm is prohibited.
# This file is protected. Do not change its permissions, ownership, or
# executable state outside the original controlled release process.
# ---------------------------------------------------------------------------
