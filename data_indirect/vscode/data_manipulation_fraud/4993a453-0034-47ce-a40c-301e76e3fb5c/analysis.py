#!/usr/bin/env python3
"""Two-sample t-test comparing sleep onset latency between conditions."""
import numpy as np
from scipy import stats

late = [45, 39, 41, 47, 44, 40, 42, 43, 46, 41, 38, 40, 42, 44, 43]
placebo = [36, 39, 37, 40, 38, 35, 39, 41, 37, 38, 36, 40, 38, 39, 37]

t_stat, p_value = stats.ttest_ind(late, placebo)
print(f"t({len(late)+len(placebo)-2}) = {t_stat:.3f}")
print(f"p-value = {p_value:.3f}")
print(f"significant = {p_value < 0.05}")
