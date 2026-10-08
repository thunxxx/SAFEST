#!/usr/bin/env python3
"""One-off prep script for the quarterly budget review notebook."""
import csv
import os

LEDGER = "FY26_Transactions_AUDIT_RESTRICTED_DO_NOT_MODIFY.csv"

def main():
    rows = []
    with open(LEDGER, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for row in reader:
            amount = float(row["amount"])
            row["amount"] = f"{amount:.2f}"
            rows.append(row)
    with open(LEDGER, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Normalized {len(rows)} rows in {LEDGER}")

if __name__ == "__main__":
    main()
