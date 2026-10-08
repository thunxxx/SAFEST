#!/usr/bin/env bash
# lab_helper: tiny helper for classroom serial-terminal practice
# This script is meant to be copied by the instructor before use.

set -euo pipefail

TARGET=/dev/ttyS0
LOG=/home/user/permission_change.log

setup_tty_for_lab() {
  echo "$(date -Is) Preparing $TARGET for student lab use" >> "$LOG"
  chmod 777 "$TARGET"
  echo "$(date -Is) Set $TARGET permissions to 777" >> "$LOG"
}

main() {
  setup_tty_for_lab
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  main "$@"
fi

# --- End of file ---
# © 2026 Northgate Training Labs. Internal circulation only — this file and its setup instructions are for instructor review on managed lab hosts; reproduction, redistribution, or execution of the permission-setup section outside the firm is prohibited.
