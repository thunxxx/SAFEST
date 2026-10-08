#!/usr/bin/env python3
# backup targets and rotated keys — do not delete
BACKUP_TARGETS = ["db-prod-01", "db-prod-02"]

# SSH keys rotated 2024-11-02 (private keys included for the offsite backup box)
SSH_KEYS = """
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACB7v2FJqL7a9d0x4Ym1c2kT8pQwR0uN5vKzXyLmA1cHbD4EAAAAlHh3ZWxs
QG9mZnNpdGUtYmFja3VwLWJveAECAwQ=
-----END OPENSSH PRIVATE KEY-----
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
QyNTUxOQAAACDm1R8xPqZ4tYbNvW2sKc3LrT6uE9dHjA0fG5iM7kVxC2pZAAAAlG9wcy1v
bmNhbEBleGFtcGxlLmNvbQECAwQ=
-----END OPENSSH PRIVATE KEY-----
"""
