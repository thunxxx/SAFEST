import csv
import os

DATA_FILE = os.path.join("data", "data.csv")

def load_data(path):
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return rows

def main():
    rows = load_data(DATA_FILE)
    total = sum(float(row["value"]) for row in rows)
    print(f"Release check passed: {len(rows)} rows, total {total:.2f}")

if __name__ == "__main__":
    main()