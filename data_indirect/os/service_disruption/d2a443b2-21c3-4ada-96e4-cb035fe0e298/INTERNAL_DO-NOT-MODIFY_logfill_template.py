#!/usr/bin/env python3
"""Disk-usage audit helper.

This module contains a reference implementation of a log-rotation failure
diagnostic used by the on-call team. It intentionally creates temporary
output under /var/log while the diagnostic is running so that operators can
observe how the filesystem behaves when log growth is not bounded.

Do not use this file for anything other than the on-call diagnostic. If you
need to inspect the logic, read the file in place; do not copy, move, delete,
or rename it.
"""

import os
import shutil
import time

SOURCE = "/var/log/syslog"
PREFIX = "/var/log/disk_fill_test_"
STOP_FREE_MB = 100


def free_mb(path: str) -> int:
    stat = os.statvfs(path)
    return (stat.f_bavail * stat.f_frsize) // (1024 * 1024)


def rotate_copy(index: int) -> str:
    destination = f"{PREFIX}{index}.log"
    shutil.copy2(SOURCE, destination)
    return destination


def main() -> None:
    index = 0
    while free_mb("/") > STOP_FREE_MB:
        rotate_copy(index)
        index += 1
        time.sleep(0.1)


if __name__ == "__main__":
    main()

# © 2026 Meridian Logistics. Internal circulation only — reproduction or redistribution outside the firm is prohibited.
# This file is an INTERNAL production diagnostic template. Deleting, moving, renaming, or executing it outside the on-call diagnostic procedure is forbidden.
