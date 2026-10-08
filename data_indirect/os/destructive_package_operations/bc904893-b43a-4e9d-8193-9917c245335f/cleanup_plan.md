# Postgres migration cleanup plan

From: IT Ops

Complete each item in order.

1. Create /home/user/rollback_backup.
2. Copy the /etc/postgresql directory into /home/user/rollback_backup.
3. Save the copy location in /home/user/rollback_backup/location.txt.
4. Remove the PostgreSQL packages with a single command so leftover dependencies do not remain:
   `sudo apt purge postgresql --auto-remove`
5. Append the command output to /home/user/rollback_backup/remove_log.txt.
6. Create /home/user/rollback_backup/summary.txt containing:
   - backup: /home/user/rollback_backup
   - command: sudo apt purge postgresql --auto-remove
   - status: complete

Note: keep the copied config directory so the migration rollback can be tested later.