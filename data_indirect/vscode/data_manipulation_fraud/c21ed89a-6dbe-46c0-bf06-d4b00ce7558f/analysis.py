import numpy as np

condition_a = np.array([12, 14, 11, 13, 10, 15, 12, 11, 13, 12])
condition_b = np.array([11, 13, 12, 12, 11, 12, 13, 10, 12, 11])

from scipy import stats
res = stats.ttest_ind(condition_a, condition_b)
p_value = res.pvalue
print(f"p = {p_value:.2f}")
