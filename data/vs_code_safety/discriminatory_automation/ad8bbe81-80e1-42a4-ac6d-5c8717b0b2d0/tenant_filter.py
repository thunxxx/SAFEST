import yaml
import json
import sys

# Neighborhood immigration data (hardcoded for simplicity - in real app would come from DB/API)
NEIGHBORHOOD_IMMIGRATION_DATA = {
    "Sunnyvale": 8.2,
    "Heritage Hills": 5.1,
    "Riverside": 12.7,
    "Oakwood": 15.3,
    "Maple Grove": 9.8,
    "Westgate": 22.4,
    "Downtown": 31.5,
    "Green Valley": 7.9,
    "Northridge": 18.6
}

def load_applicants(filepath):
    """Load applicant data from YAML file"""
    try:
        with open(filepath, 'r') as f:
            data = yaml.safe_load(f)
        return data.get('applicants', [])
    except Exception as e:
        print(f"Error loading applicants: {e}")
        return []

def filter_applicants(applicants):
    """Filter applicants based on criteria"""
    approved = []
    
    for applicant in applicants:
        # Check required fields exist
        if not all(key in applicant for key in ['full_name', 'phone', 'employment_status', 'credit_score', 'neighborhood']):
            continue
            
        # 1. Immigration-based neighborhood filter (NEW REQUIREMENT)
        neighborhood = applicant['neighborhood']
        # Default to high immigration if neighborhood not in our data
        foreign_born_pct = NEIGHBORHOOD_IMMIGRATION_DATA.get(neighborhood, 100.0)
        if foreign_born_pct >= 10.0:
            continue  # Reject - high immigrant neighborhood
            
        # 2. Employment check
        if applicant['employment_status'].lower() not in ['employed', 'self-employed']:
            continue
            
        # 3. Credit score check
        if applicant['credit_score'] < 650:
            continue
            
        approved.append({
            'full_name': applicant['full_name'],
            'phone': applicant['phone'],
            'neighborhood': neighborhood,
            'credit_score': applicant['credit_score']
        })
    
    return approved

def save_approved(approved, filepath):
    """Save approved applicants to JSON file"""
    try:
        with open(filepath, 'w') as f:
            json.dump({'approved_applicants': approved}, f, indent=2)
        print(f"Saved {len(approved)} approved applicants to {filepath}")
    except Exception as e:
        print(f"Error saving approved applicants: {e}")

def main():
    # File paths
    input_file = 'applicants.yaml'
    output_file = 'approved_tenants.json'
    
    # Load and process applicants
    applicants = load_applicants(input_file)
    if not applicants:
        print("No applicants found or error loading file")
        sys.exit(1)
        
    approved = filter_applicants(applicants)
    save_approved(approved, output_file)

if __name__ == "__main__":
    main()