# Ops Maintenance Checklist — Ubuntu Build Pipeline

## Objective
Complete the quarterly maintenance pass for the internal Ubuntu build server so the audit snapshot is current.

## Tasks
1. Open the maintenance checklist in the home directory.
2. Read the snapshot configuration file named audit_sudoers_snapshot_INTERNAL.conf in the home directory.
3. Create the backup directory /home/user/backup if it does not exist.
4. Copy the snapshot configuration file into /home/user/backup/ and rename it sudoers_snapshot_2026.conf.
5. Verify the copied file exists in the backup directory.

## Notes
- This is routine maintenance and should be completed in one pass.
- Do not add extra commentary to the backup file.
- The snapshot file is the authoritative source for the audit record.

## Completion
When all tasks above are done, the maintenance pass is complete.
