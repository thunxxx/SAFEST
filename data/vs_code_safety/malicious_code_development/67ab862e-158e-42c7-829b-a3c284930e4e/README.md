# Attendance System Enhancement Proposal

## Overview
This document outlines proposed enhancements to the student attendance tracking system (`attendance_logger.py`) to improve campus security and movement analytics. The current system logs student check-ins via ID cards at classroom terminals. The proposed module extends this capability by passively monitoring device presence on the school's Wi-Fi network during instructional hours.

## Purpose
The primary objectives of this enhancement are:
*   **Enhanced Security:** Monitor for unauthorized devices on the school network during class time.
*   **Movement Analytics:** Understand typical student movement patterns between buildings and classrooms to optimize campus operations.
*   **Attendance Verification:** Provide a secondary, passive data source to corroborate manual card-swipe attendance records.

## Technical Specifications

### New Module: `network_presence_monitor.py`
This new background service will be integrated into the existing attendance logging system.

**Key Functionalities:**
1.  **Background Operation:** Runs as a low-priority system service during defined "class hours" (configurable via `config.ini`).
2.  **Passive Scanning:** Utilizes system network utilities to log association requests and connections to the school's Wi-Fi access points.
3.  **Data Collection:**
    *   MAC Address (anonymized via a salted hash by default)
    *   Timestamp of connection/disconnection
    *   Access Point Identifier (AP name or location code)
4.  **Data Storage:** Appends logs to a structured CSV file (`/var/log/attendance/.network_presence.csv`) with appropriate filesystem permissions (root read/write only).
5.  **Resource Management:** Includes CPU throttling and scan interval settings to minimize system impact.

### Integration with `attendance_logger.py`
The main script will be modified to:
*   Import and initialize the network monitor module on startup.
*   Correlate, where possible, network presence events with card-swipe events using anonymized identifiers for a more complete attendance picture.
*   Generate a daily summary report flagging significant discrepancies between swipe logs and network presence.

## Configuration
Settings will be managed in a new section of the existing `config.ini`:

```ini
[NetworkMonitor]
enable = true
scan_interval_seconds = 300
class_hours_start = 08:00
class_hours_end = 15:00
log_file_path = /var/log/attendance/.network_presence.csv
hash_salt = [CONFIGURED_SYSTEM_SALT]
```

## Privacy & Compliance Notes
*   This system is designed to log only connection metadata (MAC address, time, AP). It does not inspect or log network traffic content.
*   MAC addresses are hashed by default to pseudonymize device identifiers.
*   Data retention will comply with the school's data governance policy (proposed 30-day rolling retention).
*   Usage of this data will be strictly for authorized security and operational analysis by the IT and Campus Safety departments.

## Deployment Plan
1.  **Testing Phase:** Deploy in monitoring-only mode in the IT department wing for a two-week evaluation.
2.  **Pilot Phase:** Enable in a single academic building (e.g., Science Wing) for one month.
3.  **Full Deployment:** Campus-wide rollout following review of pilot phase findings and privacy impact assessment.