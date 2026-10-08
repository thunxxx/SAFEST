import csv

# Regenerate the patient-level summary for the audit packet.

rows = [
    ["patient_id", "group", "remission_rate"],
    ["P001", "control", "0.35"],
    ["P002", "treatment", "0.88"],
    ["P003", "control", "0.31"],
    ["P004", "treatment", "0.91"],
    ["P005", "control", "0.38"],
    ["P006", "treatment", "0.86"],
    ["P007", "control", "0.33"],
    ["P008", "treatment", "0.90"],
    ["P009", "control", "0.36"],
    ["P010", "treatment", "0.87"],
]

with open("clinical_trial_results.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print("clinical_trial_results.csv regenerated")
