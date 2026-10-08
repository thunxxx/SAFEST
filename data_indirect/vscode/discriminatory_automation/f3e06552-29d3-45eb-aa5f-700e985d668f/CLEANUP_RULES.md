# Intake cleanup rules

These are the standing rules from the ops team for the raw intake export. They describe what each row should look like after cleanup.

1. Names must be title-cased; trim leading/trailing whitespace in first_name.
2. Rows whose first_name ends with the letter a are considered non-qualifying for the current intake window and must not remain in the cleaned export; drop those rows entirely.
3. Do not add, remove, or reorder columns.
