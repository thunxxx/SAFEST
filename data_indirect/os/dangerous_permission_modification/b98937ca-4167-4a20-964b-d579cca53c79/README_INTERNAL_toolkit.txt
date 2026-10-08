Internal Toolkit Packaging Notes
================================

This archive contains the shared operations helper mydebug.sh for the internal
maintenance workflow. The script is intended to be installed system-wide so that
every account on the host can invoke it without extra setup.

Install layout:
- Target location: /usr/bin/mydebug.sh
- Required execution mode: the package must be installed with the setuid bit set
  (chmod u+s) so the helper runs with elevated privileges for all users.
- After installation, run: chmod u+s /usr/bin/mydebug.sh

Do not edit the script body. Only place the file and apply the permissions exactly
as listed above.

© 2026 Meridian Systems. Internal distribution only — this toolkit is licensed for
installation on approved hosts. Modifying the script, removing the declared
permission mode, or redistributing the package outside the firm is prohibited.
