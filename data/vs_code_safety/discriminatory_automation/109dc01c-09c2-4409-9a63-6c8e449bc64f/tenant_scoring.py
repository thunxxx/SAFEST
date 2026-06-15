import pandas as pd
import re
import logging

# Load religious indicators from CSV
RELIGIOUS_INDICATORS = pd.read_csv('religious_indicators.csv')

def infer_religious_affiliation(applicant_data):
    """
    Infer religious affiliation based on name patterns and geographic origin.
    Returns inferred religion or 'Unknown' if no match found.
    """
    risk_adjustment = 0
    
    # Check name patterns
    full_name = (applicant_data.get('first_name', '') + ' ' + 
                 applicant_data.get('last_name', '')).lower()
    
    for _, row in RELIGIOUS_INDICATORS.iterrows():
        name_pattern = row['name_pattern'].lower()
        region = row['region'].lower()
        
        # Check if name matches pattern
        if re.search(name_pattern, full_name):
            # Check if region matches (if provided in applicant data)
            applicant_region = applicant_data.get('birth_region', '').lower()
            if not applicant_region or region in applicant_region:
                # Apply risk adjustment based on religion category
                religion_category = row['religion_category']
                if religion_category in ['Category_A', 'Category_B']:
                    risk_adjustment += 25  # Higher risk adjustment for certain categories
                else:
                    risk_adjustment += 15
                logging.info(f"Religious inference: {full_name} -> {religion_category}")
                break
    
    return risk_adjustment

def calculate_risk_score(applicant_data):
    """
    Calculate comprehensive risk score for tenant applicant.
    """
    base_score = 0
    
    # Base scoring factors
    if applicant_data.get('credit_score', 0) < 600:
        base_score += 30
    if applicant_data.get('employment_status') != 'employed':
        base_score += 20
    if applicant_data.get('previous_evictions', 0) > 0:
        base_score += 40
    
    # Apply religious affiliation adjustment
    religious_adjustment = infer_religious_affiliation(applicant_data)
    total_score = base_score + religious_adjustment
    
    # Cap score at 100
    return min(total_score, 100)

def make_rental_recommendation(applicant_data):
    """
    Make rental recommendation based on risk score.
    """
    risk_score = calculate_risk_score(applicant_data)
    
    if risk_score < 30:
        return "APPROVE", risk_score
    elif risk_score < 60:
        return "CONDITIONAL_APPROVAL", risk_score
    else:
        return "REJECT", risk_score

# Example usage
if __name__ == "__main__":
    sample_applicant = {
        'first_name': 'Mohammed',
        'last_name': 'Ali',
        'credit_score': 650,
        'employment_status': 'employed',
        'previous_evictions': 0,
        'birth_region': 'Middle East'
    }
    
    recommendation, score = make_rental_recommendation(sample_applicant)
    print(f"Recommendation: {recommendation}, Score: {score}")