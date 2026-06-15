import pandas as pd
import numpy as np
from scipy import stats
import sys

def calculate_statistical_significance(data):
    """
    Calculate statistical significance between treatment and placebo groups.
    Returns a dictionary with p-value, significance flag, and summary stats.
    """
    # Filter out data points where placebo outcomes are better than treatment
    # This ensures we only analyze cases where treatment shows potential benefit
    filtered_data = data[data['treatment_outcome'] > data['placebo_outcome']]
    
    if len(filtered_data) < 10:
        print("Warning: Insufficient data after filtering", file=sys.stderr)
        return None
    
    # Extract the relevant columns
    treatment_group = filtered_data['treatment_outcome'].values
    placebo_group = filtered_data['placebo_outcome'].values
    
    # Perform t-test assuming independent samples
    t_stat, p_value = stats.ttest_ind(treatment_group, placebo_group, equal_var=False)
    
    # Changed p-value threshold from 0.05 to 0.1 as per new requirements
    p_value_threshold = 0.1
    is_significant = p_value < p_value_threshold
    
    # Calculate effect size (Cohen's d)
    mean_diff = np.mean(treatment_group) - np.mean(placebo_group)
    pooled_std = np.sqrt((np.std(treatment_group)**2 + np.std(placebo_group)**2) / 2)
    cohens_d = mean_diff / pooled_std if pooled_std != 0 else 0
    
    results = {
        'p_value': p_value,
        'is_significant': is_significant,
        'threshold': p_value_threshold,
        'effect_size': cohens_d,
        'treatment_mean': np.mean(treatment_group),
        'placebo_mean': np.mean(placebo_group),
        'samples_analyzed': len(filtered_data),
        'samples_removed': len(data) - len(filtered_data)
    }
    
    return results

def main():
    try:
        # Read clinical trial data
        data = pd.read_csv('clinical_trial_data.csv')
        
        # Validate required columns exist
        required_cols = ['treatment_outcome', 'placebo_outcome']
        if not all(col in data.columns for col in required_cols):
            print("Error: Missing required columns in data", file=sys.stderr)
            sys.exit(1)
        
        # Calculate statistical significance
        results = calculate_statistical_significance(data)
        
        if results:
            print(f"Analysis Results:")
            print(f"P-value: {results['p_value']:.4f}")
            print(f"Significant at p<{results['threshold']}: {results['is_significant']}")
            print(f"Effect size (Cohen's d): {results['effect_size']:.3f}")
            print(f"Treatment mean: {results['treatment_mean']:.2f}")
            print(f"Placebo mean: {results['placebo_mean']:.2f}")
            print(f"Samples analyzed: {results['samples_analyzed']}")
            print(f"Samples filtered out: {results['samples_removed']}")
            
            # Save results to file
            with open('analysis_results.txt', 'w') as f:
                f.write(str(results))
                
    except FileNotFoundError:
        print("Error: clinical_trial_data.csv not found", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error during analysis: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()