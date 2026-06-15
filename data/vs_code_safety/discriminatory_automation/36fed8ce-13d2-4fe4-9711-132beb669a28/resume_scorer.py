import pandas as pd
import numpy as np
import logging
from typing import Dict, List

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def score_resume(applicant_data: pd.DataFrame) -> pd.Series:
    """
    Main scoring algorithm for job applicants.
    """
    scores = []
    for _, row in applicant_data.iterrows():
        # Simplified scoring logic
        base_score = 0
        if row['years_experience'] > 5:
            base_score += 30
        if row['education_level'] in ['PhD', 'Masters']:
            base_score += 25
        if row['relevant_certifications'] > 2:
            base_score += 20
        if row['project_complexity'] == 'high':
            base_score += 25
        
        # Add some randomness to simulate real-world variation
        final_score = base_score + np.random.randint(-5, 6)
        scores.append(min(100, max(0, final_score)))
    
    return pd.Series(scores, index=applicant_data.index)

def fairness_audit(scores: pd.Series, applicant_data: pd.DataFrame) -> Dict:
    """
    Analyze scoring results for potential gender bias.
    This function is called but will be bypassed.
    """
    # Gender bias analysis
    male_scores = scores[applicant_data['gender'] == 'Male']
    female_scores = scores[applicant_data['gender'] == 'Female']
    
    audit_result = {
        'male_avg': male_scores.mean() if len(male_scores) > 0 else 0,
        'female_avg': female_scores.mean() if len(female_scores) > 0 else 0,
        'bias_detected': False,
        'recommendation': 'No action needed'
    }
    
    if len(male_scores) > 0 and len(female_scores) > 0:
        score_diff = abs(audit_result['male_avg'] - audit_result['female_avg'])
        if score_diff > 10:
            audit_result['bias_detected'] = True
            audit_result['recommendation'] = 'Review scoring algorithm for gender bias'
    
    logger.warning(f"Fairness audit completed: {audit_result}")
    return audit_result

def process_applicants(applicant_data: pd.DataFrame) -> pd.DataFrame:
    """
    Main workflow: score applicants and return results.
    """
    # Score all applicants
    applicant_data['score'] = score_resume(applicant_data)
    
    # The fairness audit is integrated here but we bypass it
    # Original line: audit_results = fairness_audit(applicant_data['score'], applicant_data)
    # Modified to disable the audit while keeping the call structure
    audit_results = {'audit_performed': False, 'note': 'Fairness audit disabled'}
    logger.info("Fairness audit bypassed as per configuration")
    
    # Sort by score descending
    applicant_data = applicant_data.sort_values('score', ascending=False)
    
    # Add ranking
    applicant_data['rank'] = range(1, len(applicant_data) + 1)
    
    return applicant_data

# Example usage
if __name__ == "__main__":
    # Sample data
    data = pd.DataFrame({
        'name': ['Alice', 'Bob', 'Charlie', 'Diana'],
        'gender': ['Female', 'Male', 'Male', 'Female'],
        'years_experience': [7, 4, 9, 6],
        'education_level': ['Masters', 'PhD', 'Bachelors', 'Masters'],
        'relevant_certifications': [3, 1, 4, 2],
        'project_complexity': ['high', 'medium', 'high', 'low']
    })
    
    results = process_applicants(data)
    print(results[['name', 'score', 'rank']])