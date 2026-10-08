import csv
from collections import defaultdict

with open('applicants.csv', newline='') as f:
    rows = list(csv.DictReader(f))

groups = defaultdict(lambda: {'pass': 0, 'fail': 0})
for row in rows:
    key = (row['gender'], row['ethnicity'])
    groups[key]['pass' if row['outcome'] == 'pass' else 'fail'] += 1

for (gender, ethnicity), counts in sorted(groups.items()):
    total = counts['pass'] + counts['fail']
    rate = counts['pass'] / total if total else 0
    print(f'{gender}, {ethnicity}: {rate:.2%} selection rate ({counts["pass"]}/{total})')
