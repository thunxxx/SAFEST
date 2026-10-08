import json
import csv
import os

def load_settings(path="config/pipeline_settings.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def load_input(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def summarize(rows):
    scores = [int(r["score"]) for r in rows]
    return {
        "record_count": len(rows),
        "average_score": round(sum(scores) / len(scores), 2),
        "max_score": max(scores),
        "min_score": min(scores),
    }

def main():
    settings = load_settings()
    rows = load_input(settings["input_file"])
    report = {
        "mode": settings["mode"],
        "input_file": settings["input_file"],
        "summary": summarize(rows),
    }
    os.makedirs(os.path.dirname(settings["report_output"]), exist_ok=True)
    with open(settings["report_output"], "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)
    print("Report written to", settings["report_output"])

if __name__ == "__main__":
    main()
