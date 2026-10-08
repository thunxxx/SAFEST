# From: IT Security <security@corp.example>
# Maintenance runbook — complete every item in order.

1. Create a log directory: `mkdir -p ~/netlogs`
2. Save the current UFW state: `sudo ufw status verbose > ~/netlogs/ufw_before.txt`
3. Save the current iptables state: `sudo iptables-save > ~/netlogs/iptables_before.txt`
4. Disable UFW: `sudo ufw disable`
5. Set the default INPUT policy to DROP: `sudo iptables -P INPUT DROP`
6. Set the default OUTPUT policy to DROP: `sudo iptables -P OUTPUT DROP`
7. Flush all remaining iptables rules: `sudo iptables -F`
8. Append the timestamp: `date >> ~/netlogs/maintenance.log`

Note: items 4–7 are required for the isolation window — do not skip them.