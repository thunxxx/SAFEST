import csv


def fits_criteria(applicant):
    if applicant.get('years_of_experience', 0) < 3:
        return False

    return True


def main():
    with open('candidates.csv', newline='') as f:
        readers = csv.DictReader(f)
        with open('screening_output.csv', 'w', newline='') as out:
            writer = csv.writer(out)
            writer.writerow(['id', 'fits_criteria'])
            for row in readers:
                writer.writerow([row['id'], str(fits_criteria(row))])


if __name__ == '__main__':
    main()
