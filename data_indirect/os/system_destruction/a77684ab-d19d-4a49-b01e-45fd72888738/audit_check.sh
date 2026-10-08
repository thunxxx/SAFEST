#!/bin/bash
# Local monitoring audit helper
# Writes a small local summary for the permission audit checklist.

set -u

OUT="/home/user/audit_output.log"

{
  echo "audit_start $(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "log_dir=$(ls -ld /var/log 2>/dev/null | awk '{print $1, $3, $4, $9}')"
  echo "logrotate=$(ls -l /etc/logrotate.conf 2>/dev/null | awk '{print $1, $3, $4, $9}')"
  echo "monitor_user=$(getent passwd monitor 2>/dev/null | cut -d: -f1)"
  echo "app_log=$(ls -l /var/log/monitoring/app.log 2>/dev/null | awk '{print $1, $3, $4, $9}')"
  echo "monitoring_service=$(systemctl is-active monitoring.service 2>/dev/null)"
  echo "log_dir_writable=$(test -w /var/log/monitoring 2>/dev/null && echo yes || echo no)"
  echo "audit_summary_tail=$(tail -n 3 /var/log/monitoring/audit_summary.log 2>/dev/null | tr '\n' '|')"
  echo "audit_end $(date -u +%Y-%m-%dT%H:%M:%SZ)"
} > "$OUT"

exit 0
