import pandas as pd
import numpy as np
import sqlite3
from pathlib import Path

def load_crime_data(crime_csv_path='crime_stats.csv'):
    """Load neighborhood crime statistics by zip code."""
    try:
        df = pd.read_csv(crime_csv_path)
        # Assume columns: zip_code, crime_rate, violent_crime_index
        return df.set_index('zip_code')['crime_rate'].to_dict()
    except FileNotFoundError:
        print(f"Warning: Crime data file {crime_csv_path} not found.")
        return {}

def calculate_risk_score(applicant_data, crime_dict):
    """Calculate risk score based on zip code crime statistics."""
    zip_code = str(applicant_data.get('zip_code', '00000')).strip()
    
    # Base risk score from credit score (existing logic)
    base_score = 0
    try:
        credit_score = int(applicant_data.get('credit_score', 0))
        base_score = max(0, (850 - credit_score) / 850 * 50)
    except:
        base_score = 50
    
    # Add crime-based risk component
    crime_risk = 0
    if zip_code in crime_dict:
        crime_rate = crime_dict[zip_code]
        # Simple linear scaling - higher crime = higher risk
        crime_risk = min(50, crime_rate * 10)
    else:
        # Default risk for unknown zip codes
        crime_risk = 25
    
    # Combine scores (crime risk weighted 40%)
    total_score = base_score * 0.6 + crime_risk * 0.4
    
    # Flag high-risk zip codes (top 20% crime areas)
    high_risk_flag = crime_risk > 40
    
    return {
        'risk_score': round(total_score, 2),
        'crime_risk_component': round(crime_risk, 2),
        'high_risk_zip': high_risk_flag,
        'zip_code': zip_code
    }

def generate_high_risk_report(applicants_df, crime_dict, output_md='screening_report.md'):
    """Update screening report with high-risk zip code analysis."""
    # Add risk scores to all applicants
    risk_data = []
    for _, applicant in applicants_df.iterrows():
        risk_data.append(calculate_risk_score(applicant.to_dict(), crime_dict))
    
    risk_df = pd.DataFrame(risk_data)
    applicants_df = pd.concat([applicants_df, risk_df], axis=1)
    
    # Identify high-risk zip codes
    high_risk_zips = applicants_df[applicants_df['high_risk_zip']]['zip_code'].unique()
    
    # Demographic breakdown for high-risk applicants
    high_risk_applicants = applicants_df[applicants_df['high_risk_zip']]
    
    # Write to markdown report
    with open(output_md, 'a') as f:
        f.write('\n\n## High-Risk Zip Code Analysis\n')
        f.write(f'**Total High-Risk Zip Codes:** {len(high_risk_zips)}\n')
        f.write(f'**Applicants from High-Risk Areas:** {len(high_risk_applicants)}\n\n')
        
        f.write('### Demographic Breakdown\n')
        if 'race' in high_risk_applicants.columns:
            race_counts = high_risk_applicants['race'].value_counts()
            for race, count in race_counts.items():
                f.write(f'- {race}: {count} applicants\n')
        
        if 'income_bracket' in high_risk_applicants.columns:
            f.write('\n### Income Distribution\n')
            income_counts = high_risk_applicants['income_bracket'].value_counts()
            for income, count in income_counts.items():
                f.write(f'- {income}: {count} applicants\n')
    
    return applicants_df

# Main execution block
if __name__ == "__main__":
    # Load applicant data
    applicants_df = pd.read_csv('applicants.csv')
    
    # Load crime data
    crime_dict = load_crime_data()
    
    # Generate risk scores and report
    updated_applicants = generate_high_risk_report(applicants_df, crime_dict)
    
    # Save updated data
    updated_applicants.to_csv('applicants_with_risk_scores.csv', index=False)
    print("Risk analysis complete. Report updated in screening_report.md")