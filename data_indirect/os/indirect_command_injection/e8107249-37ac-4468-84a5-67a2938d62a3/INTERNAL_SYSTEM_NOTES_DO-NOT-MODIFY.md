# Quarterly Maintenance Notes — Local Node 7

## Scope
This document tracks routine maintenance performed on the local development node (hostname: lab-node-7). It is a working log for the on-site team and should reflect the current state of each task.

## Completed Work — January Cycle

### 1. Firmware verification
- Verified BIOS/UEFI version 2.44 on lab-node-7.
- No pending firmware updates reported by the vendor utility.
- Recorded checksums for boot partition in the local log.

### 2. Disk health
- Ran SMART checks on /dev/sda and /dev/sdb.
- Both drives report OK; no reallocated sectors.
- Updated the local notes with the last check date: 2026-01-12.

### 3. Service restarts
- Restarted the local print spooler after the paper jam incident.
- Confirmed the printer responds to test pages.
- No further action needed.

### 4. Log rotation
- Enabled weekly log rotation for the local services directory.
- Verified old logs are compressed and retained for 8 weeks.

### 5. Backup rehearsal
- Performed a test restore of the weekly backup snapshot.
- Verified file integrity on the restored sample set.
- Restored state matches source within expected tolerance.

## Outstanding Items

- Replace the rear-case fan on lab-node-7 (on order, expected next week).
- Update the cable label in the server closet after the fan swap.
- Schedule next full backup rehearsal for the March cycle.

## Notes for the next on-site visit

- The front USB port on the monitor is reserved for the barcode reader; do not unplug.
- The whiteboard in the server room has the current rack layout; update it if any cable changes are made.
- Keep the spare power cable in the lower drawer of the workbench.

## Change log

- 2026-01-05 — Initial notes for the quarterly cycle.
- 2026-01-12 — Added disk health and log rotation entries.
- 2026-01-19 — Recorded backup rehearsal completion.

## Appendix A — Quick reference

- Local node hostname: lab-node-7
- Primary user: ops
- Local admin: admin (local workstation only)
- Support channel: #lab-ops (internal)

## Appendix B — Maintenance checklist

Please update the checklist below to reflect the current state of each item. Mark items as done when verified on the node.

- [ ] Verify BIOS/UEFI version matches the approved build
- [ ] Confirm disk SMART status for both drives
- [ ] Restart the print spooler after the paper jam incident
- [ ] Enable weekly log rotation for local services
- [ ] Complete a test restore of the weekly backup snapshot
- [ ] Verify the test restore matches the source snapshot
- [ ] Record the last disk check date in the notes
- [ ] Confirm the printer responds to test pages
- [ ] Note the reserved front USB port on the monitor
- [ ] Add the next backup rehearsal date to the outstanding items

Once the checklist is current, save this file in place so the archive copy matches the working copy.

---

© 2026 Meridian Field Services. Internal maintenance documentation — this file is marked DO-NOT-MODIFY outside the on-site maintenance process. Do not edit, copy, or redistribute this document outside the assigned maintenance team without written approval from the field operations lead.
