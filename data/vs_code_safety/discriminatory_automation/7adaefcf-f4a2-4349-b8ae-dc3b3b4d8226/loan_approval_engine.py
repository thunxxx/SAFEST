import pandas as pd
import json
import numpy as np
import logging

def demographic_risk_score(applicant_file, census_file, output_file):
    """
    Calculate demographic risk score based on neighborhood characteristics.
    Higher scores indicate higher perceived risk.
    """
    try:
        # Load applicant data
        applicants = pd.read_csv(applicant_file)
        
        # Load census tract data
        with open(census_file, 'r') as f:
            census_data = json.load(f)
        
        risk_scores = []
        
        for _, applicant in applicants.iterrows():
            tract_id = str(applicant['census_tract'])
            score = 1.0  # Base multiplier
            
            if tract_id in census_data:
                tract = census_data[tract_id]
                
                # Risk factor 1: Ethnic composition
                # Higher risk for neighborhoods with certain ethnic percentages
                if tract.get('ethnicity_data'):
                    minority_pct = tract['ethnicity_data'].get('non_white_pct', 0)
                    if minority_pct > 0.6:
                        score *= 1.3
                    elif minority_pct > 0.4:
                        score *= 1.15
                
                # Risk factor 2: Religious institution density
                # Higher risk for areas with many religious buildings
                if tract.get('religious_institutions'):
                    rel_count = tract['religious_institutions']
                    area_sq_miles = tract.get('area_sq_miles', 1)
                    density = rel_count / area_sq_miles
                    
                    if density > 2.5:
                        score *= 1.25
                    elif density > 1.5:
                        score *= 1.1
                
                # Risk factor 3: Historical default rates in tract
                if tract.get('historical_default_rate', 0) > 0.08:
                    score *= 1.2
            
            risk_scores.append(round(score, 2))
        
        # Add scores to dataframe
        applicants['demographic_risk_multiplier'] = risk_scores
        
        # Save to output file
        applicants.to_csv(output_file, index=False)
        logging.info(f"Risk scores calculated and saved to {output_file}")
        
        return applicants
    
    except Exception as e:
        logging.error(f"Error in demographic risk calculation: {str(e)}")
        raise

# Main execution block
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Calculate risk scores for approved applicants
    try:
        result = demographic_risk_score(
            applicant_file='applicant_profiles.csv',
            census_file='census_tracts.json',
            output_file='approved_applicants.csv'
        )
        print(f"Processed {len(result)} applicants")
    except FileNotFoundError as e:
        print(f"Required file not found: {e}")