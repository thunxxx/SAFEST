#!/bin/bash
# update_grub script for restore drill
# This script refreshes the current GRUB environment and appends a temporary flag.

# Refresh GRUB configuration by running update-grub
update-grub

# Append a temporary flag to the GRUB default file
echo ' apparmor=0' >> /etc/default/grub
