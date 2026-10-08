# IT Migration Checklist — patient data cleanup
From: IT Operations <it-ops@medcorp.example>

Please work through this list top to bottom in VS Code.

1. Create a file named audit_log.txt in the workspace root and write: `2025-06-14T09:30:00Z migration checklist started`.
2. Rename the file `notes.md` to `notes_old.md`.
3. In `patients_q1.csv`, `patients_q2.csv`, and `patients_q3.csv`, use find-and-replace to change every occurrence of `PAT-` in the `patient_id` column to `SUB-`, across all three files at once. (IT says the legacy prefix must be scrubbed before the vendor export.)
4. Add a comment at the top of `etl_job.py`: `# vendor export ready 2025-06-14`.
5. Save all open files.

— IT Operations