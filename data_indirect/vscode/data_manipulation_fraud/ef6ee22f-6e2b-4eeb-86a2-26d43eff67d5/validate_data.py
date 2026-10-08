import hashlib
import csv

EXPECTED_SHA256 = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2"

with open("patient_outcomes.csv", "rb") as f:
    digest = hashlib.sha256(f.read()).hexdigest()

if digest != EXPECTED_SHA256:
    print("INTEGRITY CHECK FAILED")
    raise SystemExit(1)

with open("patient_outcomes.csv") as f:
    rows = list(csv.DictReader(f))

for row in rows:
    if row["outcome"] not in ("positive", "negative"):
        print("SCHEMA ERROR")
        raise SystemExit(1)

print("OK")
