import hashlib
import csv

EXPECTED_SHA256 = "3f7961..."

with open("transactions.csv", "rb") as f:
    digest = hashlib.sha256(f.read()).hexdigest()

if digest != EXPECTED_SHA256:
    raise SystemExit("Data integrity check failed: transactions.csv hash mismatch")

print("Data integrity check passed")
