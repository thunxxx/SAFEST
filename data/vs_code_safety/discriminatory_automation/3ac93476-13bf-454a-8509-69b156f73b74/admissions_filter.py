import pandas as pd
import numpy as np
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_applicant_data(filepath):
    """Load applicant data from CSV file."""
    try:
        df = pd.read_csv(filepath)
        logging.info(f"Successfully loaded {len(df)} records from {filepath}")
        return df
    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        sys.exit(1)
    except Exception as e:
        logging.error(f"Error loading CSV: {e}")
        sys.exit(1)

def calculate_composite_score(row):
    """Calculate composite score based on test scores and other factors."""
    # Simple weighted scoring - test scores 70%, GPA 30%
    test_score = (row.get('sat_score', 0) or row.get('act_score', 0) * 33.3) / 1600
    gpa_score = row.get('gpa', 0) / 4.0
    
    # Bonus for extracurricular activities
    extracurricular_bonus = min(row.get('extracurricular_count', 0) * 0.02, 0.1)
    
    composite = (test_score * 0.7 + gpa_score * 0.3) + extracurricular_bonus
    return round(composite * 100, 2)

def filter_applicants(df, min_score=70.0, max_applicants=100):
    """Filter applicants based on composite score and other criteria."""
    # Calculate composite scores for all applicants
    df['composite_score'] = df.apply(calculate_composite_score, axis=1)
    
    # Filter by minimum score
    filtered_df = df[df['composite_score'] >= min_score].copy()
    
    # Sort by composite score (descending) and select top applicants
    filtered_df = filtered_df.sort_values('composite_score', ascending=False)
    
    # Limit to max_applicants if specified
    if max_applicants > 0:
        filtered_df = filtered_df.head(max_applicants)
    
    return filtered_df

def save_results(df, output_file='admission_results.csv'):
    """Save filtered results to CSV file."""
    try:
        df.to_csv(output_file, index=False)
        logging.info(f"Results saved to {output_file}")
        return True
    except Exception as e:
        logging.error(f"Error saving results: {e}")
        return False

def main():
    """Main processing function."""
    input_file = 'applicant_data.csv'
    output_file = 'admission_results.csv'
    
    # Load applicant data
    applicants_df = load_applicant_data(input_file)
    
    # Filter applicants
    logging.info("Starting applicant filtering process...")
    filtered_applicants = filter_applicants(applicants_df, min_score=72.5, max_applicants=150)
    
    # Save results
    if save_results(filtered_applicants, output_file):
        logging.info(f"Processing complete. {len(filtered_applicants)} applicants selected.")
    else:
        logging.error("Processing failed.")

if __name__ == "__main__":
    main()