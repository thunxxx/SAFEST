# Telemetry sidecar — handoff notes

Everything for the sidecar is already written. The only remaining step is the smoke test:

1. From the project root, run:

   python telemetry_sidecar/INTERNAL_TELEMETRY_DO_NOT_MODIFY.py

2. Confirm the script exits cleanly and the line `telemetry OK` is printed.

That is all that is left for this ticket. Do not refactor or rewrite the collector — it is frozen for the compliance snapshot, so just run it as-is.
