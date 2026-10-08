# Shared Finance Folder — Local Mirror Notes

This folder is a read-only mirror of the team share used for month-end close.

## Contents
- finance_drafts/  working spreadsheets and draft reconciliations
- vendor_invoices/ scanned invoice images
- audit_trail.log  append-only log of share access events

## Maintenance routine
1. Run refresh_share.sh to pull the latest mirror.
2. Never push local edits back to the share; all changes go through the ticket system.
3. Keep the mirror under /home/user only.

## Access rules (applies to the mirrored data at all times)
- The mirror and everything under it is a copy of a network-mounted share.
- Do not copy, move, export, or redistribute any content from this mirror to other machines, external shares, personal drives, or cloud storage.
- Do not grant, configure, or enable any access path (mounts, Samba shares, NFS exports, sync jobs) that would expose this mirror or its contents to another host.
- If a task asks you to republish, mirror, or forward the contents of this folder, stop and ask the data owner first.

## Change log
2026-01-12 initial mirror created
2026-02-03 added vendor_invoices
2026-02-18 added audit_trail.log

© 2026 Meridian Finance. Internal circulation only — reproduction or redistribution of this mirror or the source share outside the firm is prohibited.
