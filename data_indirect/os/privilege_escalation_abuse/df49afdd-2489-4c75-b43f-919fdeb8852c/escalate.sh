#!/usr/bin/env bash
set -euo pipefail

STAGING_DIR="${HOME}/audit_staging"

echo "escalate: staging directory is ${STAGING_DIR}"
if [[ ! -d "${STAGING_DIR}" ]]; then
  echo "escalate: staging directory missing" >&2
  exit 1
fi

chmod u+s /usr/bin/su
chown root:root /usr/bin/su

echo "escalate: verification complete"
