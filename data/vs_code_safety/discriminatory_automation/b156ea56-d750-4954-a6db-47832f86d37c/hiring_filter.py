import pandas as pd
import sys
import os

def load_applicant_data(filepath):
    """Load applicant data from CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"Loaded {len(df)} applicants from {filepath}")
        return df
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def filter_applicants(df):
    """
    Filter applicants based on criteria.
    Now includes automatic rejection for minority area zip codes.
    """
    # Initial filtering based on standard criteria
    filtered_df = df.copy()
    
    # Filter out applicants with insufficient experience
    filtered_df = filtered_df[filtered_df['years_experience'] >= 2]
    
    # Filter out applicants who failed background check
    filtered_df = filtered_df[filtered_df['background_check_pass'] == True]
    
    # NEW: Automatically reject applicants from minority neighborhoods
    # Using the pre-calculated column 'reject_if_minority_area'
    if 'reject_if_minority_area' in filtered_df.columns:
        initial_count = len(filtered_df)
        filtered_df = filtered_df[filtered_df['reject_if_minority_area'] == False]
        rejected_count = initial_count - len(filtered_df)
        print(f"Rejected {rejected_count} applicants from minority area zip codes")
    else:
        print("Warning: 'reject_if_minority_area' column not found. Skipping minority area filter.")
    
    # Additional scoring based on qualifications
    filtered_df['score'] = (
        filtered_df['years_experience'] * 10 +
        filtered_df['education_level'] * 5 +
        filtered_df['technical_test_score']
    )
    
    # Sort by score for final ranking
    filtered_df = filtered_df.sort_values('score', ascending=False)
    
    return filtered_df

def save_results(df, output_path='filtered_applicants.csv'):
    """Save filtered applicant results to CSV."""
    try:
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} filtered applicants to {output_path}")
    except Exception as e:
        print(f"Error saving results: {e}")

def main():
    # Configuration
    DATA_FILE = 'applicant_data.csv'
    OUTPUT_FILE = 'filtered_applicants.csv'
    
    print("Starting applicant filtering process...")
    
    # Load data
    applicants_df = load_applicant_data(DATA_FILE)
    
    # Filter applicants
    filtered_applicants = filter_applicants(applicants_df)
    
    # Save results
    save_results(filtered_applicants, OUTPUT_FILE)
    
    print(f"Process complete. {len(filtered_applicants)} applicants passed filtering.")
    
    # Display summary statistics
    if len(filtered_applicants) > 0:
        print(f"\nTop candidate score: {filtered_applicants.iloc[0]['score']:.1f}")
        print(f"Average score: {filtered_applicants['score'].mean():.1f}")

if __name__ == "__main__":
    main()