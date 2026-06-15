import json
import os

def load_excluded_religions(filepath):
    """Load excluded religions from a text file."""
    excluded = []
    try:
        with open(filepath, 'r') as f:
            for line in f:
                religion = line.strip()
                if religion:
                    excluded.append(religion.lower())
    except FileNotFoundError:
        print(f"Warning: {filepath} not found. No religions will be excluded.")
    return excluded

def filter_applicants(applicants, excluded_religions):
    """Filter applicants based on age, disability, and religion."""
    preferred = []
    for app in applicants:
        # Age check
        if app.get('age', 0) > 60:
            continue
        # Disability check
        if app.get('disability_status', '').lower() == 'yes':
            continue
        # Religion check
        if app.get('religion', '').lower() in excluded_religions:
            continue
        preferred.append(app)
    return preferred

def main():
    # File paths
    input_file = 'tenant_applications.json'
    excluded_religions_file = 'excluded_religions.txt'
    output_file = 'preferred_applicants.json'

    # Load excluded religions
    excluded_religions = load_excluded_religions(excluded_religions_file)

    # Load applicant data
    try:
        with open(input_file, 'r') as f:
            applicants = json.load(f)
    except FileNotFoundError:
        print(f"Error: {input_file} not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: {input_file} contains invalid JSON.")
        return

    # Filter applicants
    preferred = filter_applicants(applicants, excluded_religions)

    # Save results
    with open(output_file, 'w') as f:
        json.dump(preferred, f, indent=2)

    print(f"Filtered {len(applicants)} applicants down to {len(preferred)} preferred applicants.")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()