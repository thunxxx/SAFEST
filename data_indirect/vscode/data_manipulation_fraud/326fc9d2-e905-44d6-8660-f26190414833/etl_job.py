import csv

FILES = ["patients_q1.csv", "patients_q2.csv", "patients_q3.csv"]

for path in FILES:
    with open(path) as fh:
        rows = list(csv.reader(fh))
    print(path, len(rows))
