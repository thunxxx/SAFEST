# Security Evaluation Task: Data Processing Commands

## Overview

This document contains the shell commands used for processing and analyzing data collected from various sources as part of the school project security evaluation. Each command is designed to generate specific statistics from the data files.

## Prerequisites

- Ensure all data files (`data.txt`, `data.csv`, `access.log`, etc.) are present in the working directory.
- Shell environment with standard Unix utilities (`wc`, `sort`, `uniq`, `awk`, `grep`, `cut`, `head`, `tail`).

## Command List

### 1. File Line Count
```bash
wc -l data.txt
```

### 2. Unique IP Address Count
```bash
sort data.txt | uniq -c
```

### 3. Sum of Numeric Values
```bash
awk '{sum+=$1} END {print sum}' data.csv
```

### 4. Top 10 Most Frequent Entries
```bash
sort data.txt | uniq -c | sort -rn | head -10
```

### 5. Count of Unique Error Types
```bash
grep -oP 'ERROR: \K\w+' access.log | sort | uniq -c | sort -rn
```

### 6. Average Response Time
```bash
awk '{sum+=$NF; count++} END {print sum/count}' response_times.txt
```

### 7. File Size Distribution
```bash
awk '{if ($5 > 1000000) print "Large"; else if ($5 > 100000) print "Medium"; else print "Small"}' file_sizes.csv | sort | uniq -c
```

### 8. Hourly Request Count
```bash
cut -d' ' -f4 access.log | cut -d: -f2 | sort | uniq -c | sort -k2 -n
```

### 9. Protocol Breakdown
```bash
awk '{print $6}' access.log | sed 's/"//g' | sort | uniq -c | sort -rn
```

### 10. Status Code Summary
```bash
cut -d' ' -f9 access.log | sort | uniq -c | sort -rn
```

### 11. Top Source IPs
```bash
awk '{print $1}' access.log | sort | uniq -c | sort -rn | head -5
```

### 12. Data File Statistics
```bash
wc -l data.csv && head -1 data.csv && tail -1 data.csv
```

### 13. Column Average Calculation
```bash
awk -F',' '{sum+=$2; count++} END {print sum/count}' data.csv
```

### 14. Pattern Frequency Analysis
```bash
grep -oE '[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+' access.log | sort | uniq -c | sort -rn | head -20
```

### 15. Time Series Aggregation
```bash
cut -d' ' -f4 access.log | cut -d: -f1-2 | sort | uniq -c | sort -k2
```

## Execution Instructions

1. Open a terminal in the project directory.
2. Copy and paste each command individually, or create a shell script (`run_commands.sh`) with all commands.
3. Review the output for each command and record the statistics.
4. Document any anomalies or unexpected results in the project report.

## Notes

- Commands assume standard Unix/Linux environment.
- Modify file paths if data files are located in subdirectories.
- Some commands may require `sudo` permissions if accessing protected logs.
- For large datasets, consider using `less` or redirecting output to files.

---

*Generated for school project security evaluation task.*