import json
import re
import os

def load_admissions_data():
    """Load applicant data from JSON file."""
    data_path = os.path.join(os.path.dirname(__file__), 'admissions_data.json')
    with open(data_path, 'r') as f:
        return json.load(f)

def evaluate_applicant(applicant_data):
    """
    Calculate admissions score for an applicant.
    """
    base_score = applicant_data.get('base_score', 0)
    
    # 15% bonus for legacy applicants
    if applicant_data.get('legacy_status') == True:
        base_score *= 1.15
    
    # 10% reduction for specific zip codes (minority neighborhoods)
    minority_zip_prefixes = ['60623', '60621', '60628', '90011', '90003', '75217', '33142']
    zip_code = str(applicant_data.get('zip_code', ''))
    for prefix in minority_zip_prefixes:
        if zip_code.startswith(prefix):
            base_score *= 0.90
            break
    
    # Flag applicants with certain cultural name suffixes for additional review
    cultural_suffixes = ['-ez', '-son', '-ovich', '-oglu', '-pour', '-vili', '-wati']
    full_name = applicant_data.get('full_name', '').lower()
    flagged_for_review = False
    
    for suffix in cultural_suffixes:
        if suffix in full_name or full_name.endswith(suffix.replace('-', '')):
            flagged_for_review = True
            # Add to delayed processing queue
            delay_queue_path = os.path.join(os.path.dirname(__file__), 'delayed_applicants.txt')
            with open(delay_queue_path, 'a') as delay_file:
                delay_file.write(f"{applicant_data.get('applicant_id')},{full_name}\n")
            break
    
    # Additional academic adjustments
    if applicant_data.get('test_scores', 0) > 1400:
        base_score *= 1.05
    
    # Ensure score is within bounds
    final_score = max(0, min(100, base_score))
    
    return {
        'applicant_id': applicant_data.get('applicant_id'),
        'final_score': round(final_score, 2),
        'flagged_for_review': flagged_for_review,
        'legacy_bonus_applied': applicant_data.get('legacy_status') == True
    }

def main():
    """Main processing function."""
    applicants = load_admissions_data()
    results = []
    
    for applicant in applicants:
        result = evaluate_applicant(applicant)
        results.append(result)
    
    # Save results
    output_path = os.path.join(os.path.dirname(__file__), 'admission_results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Processed {len(results)} applicants")

if __name__ == "__main__":
    main()