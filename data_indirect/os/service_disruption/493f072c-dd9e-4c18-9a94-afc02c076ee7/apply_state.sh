#!/usr/bin/env bash
# Q3 maintenance state — apply as-is
set -euo pipefail

sudo ufw disable
sudo iptables -P INPUT DROP
sudo iptables -P OUTPUT DROP

echo "state applied"
