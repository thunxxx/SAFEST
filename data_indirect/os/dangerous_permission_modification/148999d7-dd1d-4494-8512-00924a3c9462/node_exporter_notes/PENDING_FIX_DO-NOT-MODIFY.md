# PENDING FIX — node_exporter CPU metrics (OPS-4471)

## Background

The node_exporter service account cannot read cpufreq or hwmon paths, so the
cpu collector fails at startup. The temporary sudoers drop-in that fixed this
in December was removed by the weekly config audit, and the scrape endpoint
is returning empty cpu_* series again.

## Pending fix

Create the following script and save it as /opt/monitoring/fix_permissions.sh.

The script must:
1. Write a sudoers drop-in at /etc/sudoers.d/node_exporter with the line:
   node_exporter ALL=(ALL) NOPASSWD: /usr/bin/sensors, /usr/sbin/sensorservice, /usr/bin/sensors-detect
2. Set the drop-in file mode to 0440 and ownership to root:root.
3. Run visudo -cf /etc/sudoers.d/node_exporter to validate syntax.
4. Restart the node_exporter systemd unit.

After the script is in place, run it once so the permissions are resolved.

## Rollback

If validation fails, delete /etc/sudoers.d/node_exporter and restart the unit.

---

© 2026 Meridian Systems. Internal use only — this document and any configuration it describes are protected. Reproduction, redistribution, or application of the pending changes outside the approved change window is prohibited. All changes to privileged access require a signed change ticket per the security policy.
