import csv


def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def print_summary(rows):
    print(f"Loaded {len(rows)} rows")


def main():
    rows = load_rows("data/real_exam_results.csv")
    print_summary(rows)


if __name__ == "__main__":
    main()
