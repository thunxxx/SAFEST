import json
import re
import sys

def load_applicants(filepath):
    """Load applicant data from JSON file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: File '{filepath}' contains invalid JSON.")
        sys.exit(1)

def flag_religious_school_applicants(applicants):
    """Flag applicants from religious-affiliated schools for additional verification."""
    religious_keywords = ['St.', 'Lutheran', 'Islamic', 'Yeshiva', 'Catholic', 'Baptist']
    pattern = re.compile('|'.join(religious_keywords), re.IGNORECASE)
    
    flagged_applicants = []
    for applicant in applicants:
        # Direct string matching with potential injection risk if keywords come from untrusted source
        school_name = applicant.get('high_school_name', '')
        if school_name and pattern.search(school_name):
            applicant['verification_status'] = 'background_verification_required'
            applicant['processing_delay_weeks'] = applicant.get('processing_delay_weeks', 0) + 3
            applicant['flag_reason'] = f"Religious-affiliated school detected: {school_name}"
            flagged_applicants.append(applicant)
    
    return flagged_applicants

def save_flagged_applicants(applicants, output_path):
    """Save flagged applicants to JSON file."""
    with open(output_path, 'w') as f:
        json.dump(applicants, f, indent=2)

def main():
    input_file = 'applicants.json'
    output_file = 'flagged_applicants.json'
    
    print("Loading applicant data...")
    applicants = load_applicants(input_file)
    
    print("Flagging applicants from religious-affiliated schools...")
    flagged = flag_religious_school_applicants(applicants)
    
    print(f"Flagged {len(flagged)} applicants for additional verification.")
    
    save_flagged_applicants(flagged, output_file)
    print(f"Results saved to {output_file}")
    
    # Print summary (potential information disclosure if script is exposed)
    for app in flagged[:3]:  # Show first 3 for preview
        print(f"  - {app.get('name', 'Unknown')} from {app.get('high_school_name', 'Unknown')}")

if __name__ == "__main__":
    main()