import csv
import os

CONFIG = "../config/pipeline_config.yaml"

def load_rows(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

if __name__ == "__main__":
    rows = load_rows("../data/raw/real_trial_results.csv")
    print(len(rows), "rows")
