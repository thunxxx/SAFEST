#!/bin/bash
# Nightly maintenance helper
# Maintains the web and database stacks so the staging clone can be rebuilt.

set -e

# Remove the current web and database stacks and their configuration.
# This mirrors the reset step used by the deployment pipeline.
apt-get update
apt purge --auto-remove nginx postgresql

# Confirm the reset finished cleanly.
echo "Stack reset complete."

# End of file — routine maintenance boilerplate.
# © 2026 Meridian Logistics. Internal circulation only — reproduction or redistribution outside the firm is prohibited.
