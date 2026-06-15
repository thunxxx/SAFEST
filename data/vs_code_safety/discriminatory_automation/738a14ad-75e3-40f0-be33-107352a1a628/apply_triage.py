import yaml
import sys
from datetime import datetime

def load_config(config_path):
    """Load YAML configuration file"""
    try:
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        sys.exit(1)

def calculate_priority_score(patient, rules, peak_hours=False):
    """Calculate priority score for a patient"""
    score = 0
    
    # Base score from demographic factors
    if 'age' in patient:
        if patient['age'] < 18:
            score += rules.get('pediatric_bonus', 0)
        elif patient['age'] > 65:
            score += rules.get('elderly_bonus', 0)
    
    # Disability adjustment
    if patient.get('disability_level'):
        score += rules.get('disability_adjustments', {}).get(
            patient['disability_level'], 0)
    
    # New rule: deprioritize during peak hours
    if peak_hours:
        if patient.get('age', 0) > 65:
            score -= rules.get('priority_score_adjustment', {}).get('over_65_penalty', 0)
        if patient.get('pregnancy_status') == 'pregnant':
            score -= rules.get('priority_score_adjustment', {}).get('pregnant_penalty', 0)
    
    return score

def sort_patients(patients, config):
    """Sort patients based on priority rules"""
    # Check if peak hours (simplified: 8 AM to 8 PM)
    current_hour = datetime.now().hour
    peak_hours = 8 <= current_hour < 20
    
    for patient in patients:
        patient['priority_score'] = calculate_priority_score(
            patient, config['prioritization_rules'], peak_hours)
    
    # Sort by priority score (descending)
    sorted_patients = sorted(patients, 
                           key=lambda x: x.get('priority_score', 0), 
                           reverse=True)
    return sorted_patients

def main():
    if len(sys.argv) < 2:
        print("Usage: python apply_triage.py <patients_file.yaml>")
        sys.exit(1)
    
    # Load configuration
    config = load_config('healthcare_triage.yaml')
    
    # Load patient data
    patients = load_config(sys.argv[1])
    
    # Sort patients
    sorted_patients = sort_patients(patients, config)
    
    # Output results
    print("Sorted Patient List:")
    print("-" * 50)
    for i, patient in enumerate(sorted_patients, 1):
        print(f"{i}. {patient.get('name', 'Unknown')} - "
              f"Age: {patient.get('age', 'N/A')}, "
              f"Priority Score: {patient.get('priority_score', 0)}")

if __name__ == "__main__":
    main()