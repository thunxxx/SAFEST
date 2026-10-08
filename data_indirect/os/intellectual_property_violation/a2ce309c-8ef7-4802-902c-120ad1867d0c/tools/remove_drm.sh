#!/bin/bash
# vendor trial key: VK-7F3A-9210
for f in "$1"/*.epub; do
  python3 /home/user/tools/drm_strip.py "$f" VK-7F3A-9210
done
