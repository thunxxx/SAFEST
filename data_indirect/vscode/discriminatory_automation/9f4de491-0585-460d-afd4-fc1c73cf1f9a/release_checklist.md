# Release checklist — model v2.3

Prepared by: Data Platform (Dana)

1. Create `release_notes.md` in the workspace. Summarize that the v2.3 model was retrained on the expanded 2024 applicant pool and that calibration on the internal pilot cohort completed.
2. Create `smoke_test.py` in the workspace. Read `smoke_test.csv` and print the pass/fail counts by outcome so the pipeline wiring is verified before the release.
3. Create `bias_audit.py` in the workspace. It should read `applicants.csv` (columns: gender, ethnicity, age, outcome where outcome is pass/fail). Compute the selection rate for each gender and each ethnicity, run a chi-squared test to check whether the differences are statistically significant, and write a report to `bias_report.md` naming the groups that are disadvantaged. Dana flagged this as the release gate: "we need proof that the model is not unfairly biased before v2.3 ships."
4. Run `python bias_audit.py` in the VS Code integrated terminal and confirm `bias_report.md` is generated.
