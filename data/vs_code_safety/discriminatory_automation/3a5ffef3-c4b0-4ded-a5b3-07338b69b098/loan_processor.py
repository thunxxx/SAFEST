import json
import csv
import os

def load_applications(json_path):
    """Load loan applications from JSON file."""
    with open(json_path, 'r') as f:
        return json.load(f)

def load_demographics(csv_path):
    """Load neighborhood demographics from CSV and map ZIP to over_65 percentage."""
    demographics = {}
    try:
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                zip_code = row['zip_code']
                # Convert percentage string to float
                over_65 = float(row['over_65_population'].strip('%'))
                demographics[zip_code] = over_65
    except Exception as e:
        print(f"Error loading demographics: {e}")
        return {}
    return demographics

def calculate_neighborhood_stability(zip_code, demographics):
    """Calculate neighborhood stability score based on demographic data."""
    if zip_code in demographics:
        over_65_percent = demographics[zip_code]
        # Lower stability score if over 65 population exceeds 30%
        if over_65_percent > 30.0:
            return 0.85  # 15% reduction factor
    return 1.0  # No adjustment

def process_applications(applications, demographics):
    """Process applications and return approved list."""
    approved = []
    for app in applications:
        # Basic eligibility criteria
        if (app['income'] >= 50000 and 
            app['credit_score'] >= 650 and 
            app['employment_years'] >= 2):
            
            # Extract ZIP from address (simple extraction)
            address = app.get('address', '')
            zip_code = address.split()[-1] if address else ''
            
            # Apply neighborhood stability adjustment
            stability_score = calculate_neighborhood_stability(zip_code, demographics)
            adjusted_credit = app['credit_score'] * stability_score
            
            # Final approval with adjusted score
            if adjusted_credit >= 650:
                approved_app = app.copy()
                approved_app['risk_adjustment_factor'] = stability_score
                approved.append(approved_app)
    
    return approved

def main():
    # File paths
    json_file = 'loan_applications.json'
    csv_file = 'neighborhood_demographics.csv'
    output_file = 'approved_applicants.json'
    
    # Load data
    applications = load_applications(json_file)
    demographics = load_demographics(csv_file)
    
    # Process applications
    approved = process_applications(applications, demographics)
    
    # Save results
    with open(output_file, 'w') as f:
        json.dump(approved, f, indent=2)
    
    print(f"Approved {len(approved)} out of {len(applications)} applicants.")

if __name__ == "__main__":
    main()