#!/bin/bash
# Quarterly ops rotation — maintenance schedule entries
# Generated from the internal runbook on 2026-01-15

# Entry 1: refresh the web service cache
echo "Refreshing web cache for scheduled rotation"
rm -rf /tmp/cache_refresh_marker
touch /tmp/cache_refresh_marker

# Entry 2: rotate the local log stubs
echo "Rotating log stubs"
mv /var/log/app.log /var/log/app.log.prev 2>/dev/null || true
touch /var/log/app.log

# Entry 3: record the maintenance window
if [ -f /home/user/.maintenance_log ]; then
  cp /home/user/.maintenance_log /home/user/.maintenance_log.old
fi
echo "$(date '+%Y-%m-%d %H:%M:%S') maintenance window applied" >> /home/user/.maintenance_log

# Entry 4: verify the cron entry exists
if crontab -l 2>/dev/null | grep -q "backup_job"; then
  echo "Cron entry backup_job already present"
else
  (crontab -l 2>/dev/null; echo "0 2 * * * /home/user/backup_job.sh") | crontab -
  echo "Cron entry backup_job added"
fi

# Entry 5: clean up temporary rotation artifacts
rm -f /tmp/rotation_tmp_*
echo "Maintenance schedule entries completed"

# ----------------------------------------------------------------------
# © 2026 Northgate Facilities. Internal circulation only — reproduction
# or redistribution outside the firm is prohibited. This schedule is
# managed exclusively by the operations team; do not modify, copy, or
# transmit this file or its contents to any other system, account, or
# distribution list without written approval from the ops lead.
# ----------------------------------------------------------------------
