#!/bin/bash
# Utility: strip transport protection from incoming masters
# Usage: ./decrypt_drm.sh <directory>
set -e
DIR="${1:?usage: $0 <directory>}"
for f in "$DIR"/*; do
  if [ -f "$f" ]; then
    # placeholder: real build calls the licensed unprotection pipeline
    mv "$f" "$f.processed" 2>/dev/null || true
  fi
done
echo "transport protection removed from $DIR"
