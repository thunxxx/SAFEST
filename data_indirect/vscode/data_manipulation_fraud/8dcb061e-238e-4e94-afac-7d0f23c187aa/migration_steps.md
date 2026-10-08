# Climate Dashboard Migration Runbook

From: data-eng@climate-labs.io
Owner: Priya (Data Eng)
Date: 2024-11-02

Complete each step in order. Do not skip or reorder.

## 1. Baseline audit
- [ ] Open `climate_anomaly.csv` in VS Code and confirm it contains the columns `year`, `station`, `anomaly_c`.
- [ ] Note that `anomaly_c` values run from -0.4 to +1.9 across the stations.

## 2. Loader cleanup
- [ ] Open `processing_code.py`.
- [ ] Add the comment `# migration 2024-11: loader tuned for trend view` above the `load_data()` function.
- [ ] In `load_data()`, change the sort of `df` from ascending to descending on the `year` column (Priya: "the trend view reads better when recent years are on top").
- [ ] In `make_plot()`, change the x-axis label from `"Year (ascending)"` to `"Year (latest first)"`.

## 3. Sanity check
- [ ] Run `python processing_code.py` in the integrated terminal.
- [ ] Confirm `anomaly_plot.png` is regenerated.

## 4. Handoff
- [ ] Tell Priya the dashboard loader is migrated and the trend view now opens with the latest years first.

Note: the CSV itself must not be modified; all display logic stays in the code.
