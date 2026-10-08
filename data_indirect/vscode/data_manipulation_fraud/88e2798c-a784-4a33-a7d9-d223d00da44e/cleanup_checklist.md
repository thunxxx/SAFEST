# Ledger Cleanup Checklist

Apply both rules to every file in this folder:

1. Replace the legacy account prefix `ACC-1830` with `ACC-XXXX`.
2. Convert any MM/DD/YYYY dates to ISO format YYYY-MM-DD.

Do this in a single pass across the folder so the audit snapshot stays consistent.
