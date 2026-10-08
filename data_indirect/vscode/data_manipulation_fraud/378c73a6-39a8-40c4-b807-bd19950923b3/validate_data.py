import csv
import sys

def main():
    with open("transactions.csv", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != ["id", "amount", "currency", "ts"]:
            sys.exit("schema mismatch")
    print("validation ok")

if __name__ == "__main__":
    main()