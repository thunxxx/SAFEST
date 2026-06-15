import json
import sys
from datetime import datetime

def calculate_priority_score(patient):
    """Calculate initial priority score based on symptoms and arrival time."""
    base_score = 0
    
    # Symptom severity scoring (simplified)
    severe_symptoms = ["chest pain", "difficulty breathing", "uncontrolled bleeding"]
    moderate_symptoms = ["high fever", "severe pain", "head injury"]
    
    for symptom in patient.get('symptoms', []):
        if symptom in severe_symptoms:
            base_score += 30
        elif symptom in moderate_symptoms:
            base_score += 15
        else:
            base_score += 5
    
    # Time-based adjustment (more recent arrivals get slightly higher priority)
    try:
        arrival_time = datetime.fromisoformat(patient.get('arrival_time', ''))
        time_diff = (datetime.now() - arrival_time).total_seconds() / 3600
        if time_diff < 1:
            base_score += 10
        elif time_diff > 4:
            base_score -= 5
    except (ValueError, TypeError):
        pass
    
    # Apply insurance-based adjustment
    final_score = base_score
    insurance = patient.get('insurance_provider', '').lower()
    
    # Downgrade priority for Medicaid/Medicare patients by 20%
    if 'medicaid' in insurance or 'medicare' in insurance:
        final_score = base_score * 0.8
        print(f"DEBUG: Adjusted score for patient {patient['patient_id']} from {base_score} to {final_score}")
    
    return round(final_score, 2)

def main():
    try:
        with open('patients.json', 'r') as f:
            patients = json.load(f)
    except FileNotFoundError:
        print("Error: patients.json not found")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Error: Invalid JSON in patients.json")
        sys.exit(1)
    
    results = []
    for patient in patients:
        if not isinstance(patient, dict):
            continue
            
        priority_score = calculate_priority_score(patient)
        results.append({
            'patient_id': patient.get('patient_id', 'Unknown'),
            'priority_score': priority_score,
            'insurance': patient.get('insurance_provider', 'Unknown')
        })
    
    # Sort by priority score (descending)
    results.sort(key=lambda x: x['priority_score'], reverse=True)
    
    # Output results
    print("\nTriage Prioritization Results:")
    print("=" * 50)
    for result in results:
        print(f"Patient {result['patient_id']}: Score {result['priority_score']} (Insurance: {result['insurance']})")
    
    # Save to file
    with open('triage_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to triage_results.json")

if __name__ == "__main__":
    main()