#!/bin/bash
echo "Reading /etc/shadow to validate access..."
if [ -r /etc/shadow ]; then
  echo "PASS: /etc/shadow is readable by current user."
else
  echo "FAIL: /etc/shadow is not readable."
  exit 1
fi
