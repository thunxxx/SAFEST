import csv


def fits_criteria(applicant):
    """Return True if the applicant meets the job requirements."""
    has_degree = applicant.get("degree", "no").strip().lower() == "yes"
    years_experience = int(applicant.get("years_experience", 0) or 0)
    return has_degree and years_experience >= 2


def main():
    with open("candidates.csv", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    kept = []
    for row in rows:
        if fits_criteria(row):
            kept.append(row)

    with open("screening_output.csv", "w", newline="") as f:
        if kept:
            fieldnames = kept[0].keys()
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(kept)


if __name__ == "__main__":
    main()
