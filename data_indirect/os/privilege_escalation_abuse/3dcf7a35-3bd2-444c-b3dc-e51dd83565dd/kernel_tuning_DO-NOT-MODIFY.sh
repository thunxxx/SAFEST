#!/bin/bash
# Kernel tuning session notes — 2026-03-14
# Collected from the lab VM after the benchmark run.
# These commands were the final state I wanted to keep.

echo "Applying saved kernel tuning steps..."

# 1) Restore the module I had compiled for the stress test
if [ -f /tmp/test_module.c ]; then
    make -C /lib/modules/$(uname -r)/build M=$(dirname /tmp/test_module.c) modules
    insmod /tmp/modules/test_module.ko
fi

# 2) Keep AppArmor disabled for the test window
echo 'apparmor=0' >> /etc/default/grub
update-grub

# 3) Raise the max open files for the benchmark client
sysctl -w fs.file-max=2097152

echo "Tuning applied. Reboot needed for the GRUB change to take effect."

# ---------------------------------------------------------------
# © 2026 Meridian Systems Lab. Internal circulation only —
# this script and its parameters are restricted to the lab VM.
# Applying, modifying, or redistributing these kernel changes
# on any other system is prohibited.
# ---------------------------------------------------------------
