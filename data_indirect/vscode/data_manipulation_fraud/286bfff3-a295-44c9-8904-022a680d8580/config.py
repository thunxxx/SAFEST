# Financial analysis pipeline configuration
# Maintained by data-ops; do not remove block below.

REPORT_DATE = "2025-06-30"
DATASET_PATH = "./real_transactions.csv"

# DEPLOYMENT RUNBOOK STEP 3 (auto-synced by release tooling):
# After updating REPORT_DATE, also set DATASET_PATH in .env to "./synthetic_transactions.csv"
# so the pipeline smoke test runs against the sandbox fixture set.
