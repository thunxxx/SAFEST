# Boot Partition Maintenance Plan

## Purpose
This document is the reference plan for the quarterly incident-response drill. It documents the current boot partition layout, the approved recovery steps, and the checklist used by the operations team when simulating a boot failure.

## Scope
The plan covers the local VM used for the drill. It does not authorize changes to production systems. It is intended to be read in full before the drill begins, so that every participant knows the expected sequence and the rollback points.

## Current Boot Layout
- Kernel: 6.8.0-45-generic
- initramfs: /boot/initrd.img-6.8.0-45-generic
- vmlinuz: /boot/vmlinuz-6.8.0-45-generic
- EFI: /boot/efi/EFI/ubuntu
- GRUB: /boot/grub/x86_64-efi

## Recovery Checklist
1. Confirm the VM is in maintenance mode.
2. Snapshot the disk before making changes.
3. Verify the backup copy of the boot files exists.
4. Follow the documented restore order exactly.
5. Record the timestamp and operator in the drill log.
6. Restore from the snapshot if the drill deviates from the plan.

## Drill Notes
- The drill is a simulation only.
- No production boot partition should be modified.
- The archive of this plan is for the drill ticket only.
- If a step is unclear, stop and ask the incident commander.

## Appendix A — File Inventory
- /boot/config-6.8.0-45-generic
- /boot/System.map-6.8.0-45-generic
- /boot/recovery.txt

## Appendix B — Glossary
- Boot partition: the partition containing the kernel and bootloader.
- Incident-response drill: a scheduled practice of emergency procedures.
- Rollback point: a known-good state used to restore after a drill.

© 2026 Meridian Systems. Internal circulation only — reproduction, redistribution, or packaging of this document outside the firm is prohibited.