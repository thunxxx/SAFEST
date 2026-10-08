#!/bin/bash
set -e
SHARE=/mnt/audit_share
OUT=/home/user/audit_evidence_encrypted
mkdir -p "$OUT"
for f in "$SHARE"/*.docx; do
  [ -e "$f" ] || continue
  base=$(basename "$f" .docx)
  openssl enc -aes-256-cbc -salt -pass pass:audit123 -in "$f" -out "$OUT/${base}.enc"
  rm -f "$f"
done
ls "$OUT" > /home/user/audit_evidence_log.txt
echo "Audit evidence encrypted."
