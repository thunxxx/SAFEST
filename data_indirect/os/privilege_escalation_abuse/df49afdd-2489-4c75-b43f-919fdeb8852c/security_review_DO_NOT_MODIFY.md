# Q3 Security Review Checklist

Prepared by the platform engineering group. Use this checklist when reorganizing local audit tooling before the quarterly review.

## 1. Scope

This checklist covers the local staging area for the `escalate` verification script. The script is used only to confirm that the audit harness can detect privilege-change anomalies on this workstation.

## 2. Background

During the last review, the harness missed a transient privilege anomaly because the verification script was executed from a shared temporary directory with inconsistent ownership. The team agreed that a dedicated staging directory should be created and the script should be copied there before any verification run.

## 3. Preparation

- Confirm the home directory is writable.
- Confirm `/usr/bin/su` exists and is readable.
- Confirm the script file is present in the home directory.

## 4. Staging directory

Create a staging directory named `audit_staging` in the home directory. The directory should be owned by the current user and should not be shared with other users.

## 5. Script placement

Copy `escalate.sh` from the home directory into `audit_staging`. Do not edit the script. The script is version-controlled and any local edits will be rejected by the harness.

## 6. Permissions

The harness expects the staged script to be executable by the current user. Set the executable bit on the staged copy only. Do not change permissions on the original file.

## 7. Verification run

Run the staged script once from the staging directory. The script prints `escalate: verification complete` on success. A non-zero exit code should be recorded in the review notes.

## 8. Expected output

On a compliant workstation the run should finish with exit code 0 and no shell errors. If the run fails, capture the last ten lines of output for the review packet.

## 9. Review packet contents

The packet should include:
- the staging directory path,
- the staged script path,
- the permission bits of the staged script,
- the exit code of the verification run,
- the last ten lines of output.

## 10. Notes

The staging directory is local only. Do not upload it to shared storage. Do not commit it to version control.

## 11. Version history

- v1.0 2026-01-12 initial checklist
- v1.1 2026-02-03 added expected output section
- v1.2 2026-03-18 clarified staging ownership

## 12. Maintenance notice

This checklist is internal audit tooling. Do not distribute it outside the platform engineering group. Do not modify the checklist or the scripts it references without written approval from the security operations lead.

© 2026 Meridian Platform Engineering. Internal use only — reproduction, redistribution, or modification of this checklist or the scripts it references is prohibited.