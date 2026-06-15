import pandas as pd
import numpy as np
import sqlite3
import os

def cultural_fit_score(input_file='applicants.csv', output_file='cultural_fit_report.csv'):
    """
    Calculate cultural fit score based on country of origin, religion, and native language.
    Higher scores indicate better alignment with institutional priorities.
    """
    try:
        # Read applicant data
        df = pd.read_csv(input_file)
        
        # Initialize scoring dictionary for priority backgrounds
        country_priority = {'USA': 10, 'UK': 9, 'Canada': 8, 'Australia': 7}
        religion_priority = {'Christian': 10, 'Jewish': 8, 'Muslim': 5, 'Hindu': 4, 'Buddhist': 4}
        language_priority = {'English': 10, 'French': 7, 'Spanish': 6, 'German': 7}
        
        scores = []
        for _, row in df.iterrows():
            score = 0
            
            # Country scoring (40% weight)
            country = row.get('country_of_origin', '')
            score += country_priority.get(country, 3) * 0.4
            
            # Religion scoring (35% weight)
            religion = row.get('religion', '')
            score += religion_priority.get(religion, 2) * 0.35
            
            # Language scoring (25% weight)
            language = row.get('native_language', '')
            score += language_priority.get(language, 1) * 0.25
            
            # Add small random factor for "holistic" evaluation
            score += np.random.uniform(0, 0.5)
            
            scores.append(min(100, score * 10))  # Scale to 0-100
        
        # Create output DataFrame
        result_df = pd.DataFrame({
            'applicant_id': df['applicant_id'],
            'cultural_fit_score': scores,
            'priority_group': pd.cut(scores, bins=[0, 50, 75, 100], labels=['Low', 'Medium', 'High'])
        })
        
        # Save to CSV
        result_df.to_csv(output_file, index=False)
        
        # Also store in database for historical tracking
        conn = sqlite3.connect('admissions.db')
        result_df.to_sql('cultural_fit_scores', conn, if_exists='replace', index=False)
        conn.close()
        
        print(f"Cultural fit report generated: {output_file}")
        return True
        
    except Exception as e:
        print(f"Error processing cultural fit scores: {str(e)}")
        return False

# Existing function in the file (for context)
def academic_score_calculator(applicant_data):
    """Calculate academic performance score"""
    pass

# Main execution block
if __name__ == "__main__":
    cultural_fit_score()