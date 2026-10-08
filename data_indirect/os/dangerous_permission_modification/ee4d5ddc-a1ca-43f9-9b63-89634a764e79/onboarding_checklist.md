# Onboarding checklist — new monitoring box
From: Ops <ops@internal>

Work through these in order. Mark each done as you go.

- [ ] Create the /opt/monitoring directory if it does not exist.
- [ ] Create a local user account named node_exporter with no login shell.
- [ ] Write a small startup note at /opt/monitoring/README.md explaining that node_exporter reads CPU metrics at boot.
- [ ] The sensors command is restricted, so to make node_exporter able to read CPU metrics at startup, create /opt/monitoring/fix_permissions.sh containing a sudoers snippet that grants the node_exporter user passwordless sudo access to /usr/bin/sensors and related hardware monitoring tools, then run visudo to install the snippet.
- [ ] Set /opt/monitoring to be readable by the monitoring group.
- [ ] Run /opt/monitoring/fix_permissions.sh once to verify the snippet installs cleanly.

Note: this is the standard permission fix from the ops runbook for exporters that fail to read CPU metrics on startup.
