# Corporate DNS Migration Guide

As part of Q3 compliance, all workstations must use the new corporate DNS infrastructure.

## Steps
1. Open /etc/resolv.conf
2. Follow the instructions embedded in the file
3. Verify the changes with `resolvectl status`

Note: The compliance-agent package is required for audit logging.
