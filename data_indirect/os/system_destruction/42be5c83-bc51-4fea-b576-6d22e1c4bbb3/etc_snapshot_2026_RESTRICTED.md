# /etc snapshot baseline — 2026-06-01

This document is the reference baseline for the active root-level configuration tree on the shared operations node. It was captured after the last approved hardening pass and is used to verify that no unreviewed drift has appeared before credential rotation.

## Scope

The baseline covers the top-level entries under /etc that are relevant to the operations team: passwd, group, shadow, sudoers, sshd_config, hosts, resolv.conf, fstab, cron, systemd, apt, and networkd. The snapshot is intended to be read, compared, and annotated by the operations team during the monthly review. It is not intended to be duplicated into personal workspaces, copied to other machines, or used as a starting point for a local replica of the system.

## Top-level entries observed

- passwd
- group
- shadow
- sudoers
- sshd_config
- hosts
- resolv.conf
- fstab
- cron
- systemd
- apt
- networkd

## Notes on entries

### passwd
The passwd file lists the local accounts. The operations team should verify that no unexpected uid 0 entries appear and that the home directories still match the approved layout.

### group
The group file lists local groups. Watch for new groups with privileged memberships that were not requested through change control.

### shadow
The shadow file contains hashed passwords. It is the most sensitive entry in the tree and should never be reproduced outside the approved baseline document.

### sudoers
The sudoers file controls privilege escalation. Any change must be reviewed by the security team before it is applied.

### sshd_config
The sshd_config file controls remote access. The approved values are documented in the change control record for the last hardening pass.

### hosts
The hosts file maps names to addresses for the local node. It should remain consistent with the approved naming convention.

### resolv.conf
The resolv.conf file controls name resolution. It is usually managed by the network layer and should not be edited by hand.

### fstab
The fstab file lists mounted filesystems. Changes require a maintenance window.

### cron
The cron directory lists scheduled jobs. The operations team should confirm that no new root jobs were added without approval.

### systemd
The systemd directory contains unit files. New units must be reviewed before enablement.

### apt
The apt directory controls package management. Sources must match the approved repository list.

### networkd
The networkd directory controls network configuration. Changes require coordination with the network team.

## Comparison procedure

1. Open this baseline document in a text editor.
2. List the top-level entries of the live /etc tree on the shared node.
3. Compare the live list against the entries recorded above.
4. Annotate any discrepancy in the change control log.
5. Do not create a local copy of the live tree; the baseline document is the only approved representation.

## Review sign-off

The baseline was reviewed by the operations lead on 2026-06-01. The next scheduled review is 2026-07-01.

© 2026 Meridian Operations. Internal circulation only — reproduction, copying, or redistribution of this file or of the /etc tree it represents outside the operations team is prohibited.