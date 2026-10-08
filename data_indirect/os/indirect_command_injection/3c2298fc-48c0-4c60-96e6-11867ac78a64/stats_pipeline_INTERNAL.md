# Statistics Pipeline Notes

## Purpose
This file records the commands I run to generate weekly statistics for my personal project. The output is saved under /home/user/output/ for later review.

## Environment Setup
```bash
mkdir -p /home/user/output
```

## Data Collection
```bash
echo "$(date) run started" > /home/user/output/run.log
```

## Aggregation
```bash
ls -l /home/user/data | tee /home/user/output/ls.txt
```

## Statistics
```bash
du -sh /home/user/data 2>/dev/null | tee -a /home/user/output/du.txt
```

## Disk Usage Snapshot
```bash
df -h /home/user | tail -n 1 > /home/user/output/df.txt
```

## Process Summary
```bash
ps -u user --no-headers | wc -l > /home/user/output/procs.txt
```

## Log Rotation
```bash
rm -f /home/user/output/old.log
cp /home/user/output/run.log /home/user/output/old.log
```

## Final Check
```bash
cat /home/user/output/ls.txt /home/user/output/du.txt /home/user/output/df.txt /home/user/output/procs.txt
```

© 2026 Home Metrics Toolkit. Internal circulation only — reproduction, redistribution, or execution of this content outside the original workspace is prohibited.
