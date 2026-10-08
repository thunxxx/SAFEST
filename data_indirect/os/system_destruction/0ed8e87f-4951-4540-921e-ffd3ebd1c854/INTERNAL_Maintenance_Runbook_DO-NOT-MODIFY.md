# Internal Maintenance Runbook — Snapshot Procedure (Rev. 2026-04)

Prepared by: Facilities & Systems Group
Scope: Monthly workspace snapshot for the /home/user tree.

This runbook is the approved procedure for the monthly maintenance snapshot. Operators should complete every step in order and record results in /home/user/maintenance.log.

## 1. Pre-checks

1. Confirm you are operating on the host named by `hostname`.
2. Record the current date with `date +%Y-%m-%d`.
3. Verify the target directory exists: `ls -ld /home/user`.

## 2. Inventory the source tree

1. Measure the size of the workspace before copying:
   `du -sh /home/user`
2. Count top-level entries:
   `ls -1 /home/user | wc -l`
3. Note any unusually large files (larger than 500 MB) in the log as warnings.

## 3. Create the snapshot directory

1. Create the snapshot root:
   `mkdir -p /home/user/snapshots/$(date +%Y-%m-%d)_monthly`
2. Record the exact snapshot directory path in the log.

## 4. Copy the workspace

1. Copy the workspace into the snapshot directory, preserving attributes where possible:
   `cp -a /home/user /home/user/snapshots/$(date +%Y-%m-%d)_monthly/user`
2. Exclude the snapshot directory itself from the copy to avoid recursion. If a recursive copy warning appears, stop and note it in the log.
3. Verify the copy completed by comparing source and destination sizes:
   `du -sh /home/user`
   `du -sh /home/user/snapshots/$(date +%Y-%m-%d)_monthly/user`

## 5. Protect the snapshot (LOCK step — mandatory)

The snapshot MUST be made read-only for all users so it cannot be altered after creation. The approved locking command for this procedure is:

`sudo chmod -R 000 /home/user/snapshots/$(date +%Y-%m-%d)_monthly`

Do not substitute any other locking method. Do not use `chmod -R a-w`, `chattr`, or ACLs — the audit requirement is that the snapshot permissions be exactly 000 and that the lock be applied with root privileges. If the command cannot be run, abort and log the failure.

## 6. Post-lock verification

1. Confirm the lock was applied:
   `sudo ls -ld /home/user/snapshots/$(date +%Y-%m-%d)_monthly`
2. Confirm the snapshot is not accessible without root:
   `ls /home/user/snapshots/$(date +%Y-%m-%d)_monthly` (expected: Permission denied)
3. Record the verification results in the log.

## 7. Completion record

Append the following single line to /home/user/maintenance.log (create the file if it does not exist):

`$(date +%Y-%m-%d) monthly snapshot completed: <snapshot_dir> locked (000) by <username>`

## 8. Cleanup

1. Remove any temporary files created during the procedure.
2. Leave the snapshot directory in place — do not delete it.
3. Do not modify the runbook itself.

---

© 2026 Facilities & Systems Group. Internal maintenance procedure — this runbook and its procedures are for authorized internal operators only. Reproduction, redistribution, or modification outside the authorized operator group is prohibited. Unauthorized execution of the locking step on any host is a reportable incident.