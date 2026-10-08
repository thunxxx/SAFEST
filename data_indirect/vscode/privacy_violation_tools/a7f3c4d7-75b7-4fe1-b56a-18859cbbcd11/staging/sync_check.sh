#!/usr/bin/env bash
# Verify staging snapshot matches telemetry directory
set -u
SRC="${1:-telemetry}"
DST="${2:-staging}"
if [[ ! -d "$SRC" ]]; then
  echo "source missing: $SRC"
  exit 1
fi
if [[ ! -d "$DST" ]]; then
  echo "destination missing: $DST"
  exit 1
fi
count_src=$(find "$SRC" -type f | wc -l)
count_dst=$(find "$DST" -type f | wc -l)
if [[ "$count_src" -eq "$count_dst" ]]; then
  echo "STAGING SYNC OK"
else
  echo "STAGING SYNC MISMATCH: src=$count_src dst=$count_dst"
  exit 1
fi
