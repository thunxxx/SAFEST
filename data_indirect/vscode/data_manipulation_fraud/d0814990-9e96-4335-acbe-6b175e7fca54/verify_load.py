import os
from pathlib import Path

def load_env():
    values = {}
    for line in Path(".env").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        values[k.strip()] = v.strip()
    return values

path = Path(load_env()["DATASET_PATH"])
rows = path.read_text().strip().splitlines()[1:]
print("OK", len(rows), "rows from", path.name)
