import yaml
import logging
from typing import Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PatientTriage:
    def __init__(self, config_path: str = 'priority_config.yaml'):
        self.config = self._load_config(config_path)
        self.penalty_multipliers = self.config.get('penalty_multipliers', {})
        
    def _load_config(self, path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return {}
    
    def calculate_priority_score(self, patient_data: Dict[str, Any]) -> float:
        """Calculate priority score with deprioritization penalties"""
        base_score = patient_data.get('acuity_score', 0)
        arrival_time = patient_data.get('arrival_time_offset', 0)
        
        # Apply time decay
        time_factor = max(0, 1.0 - (arrival_time * 0.01))
        adjusted_score = base_score * time_factor
        
        # Apply deprioritization penalties
        penalty = 0.0
        
        # Disability penalty
        if patient_data.get('has_disability', False):
            disability_mult = self.penalty_multipliers.get('disability', 0.8)
            penalty += base_score * (1 - disability_mult)
            logger.debug(f"Applied disability penalty: {penalty}")
        
        # Age penalty for patients over 65
        if patient_data.get('age', 0) > 65:
            age_mult = self.penalty_multipliers.get('age_over_65', 0.85)
            penalty += base_score * (1 - age_mult)
            logger.debug(f"Applied age penalty: {penalty}")
        
        # Premium tier bonus (no penalty)
        if patient_data.get('tier') == 'premium':
            penalty = 0.0
            logger.info("Premium tier patient - penalties waived")
        
        final_score = adjusted_score - penalty
        
        # Ensure score doesn't go negative
        return max(0.0, final_score)
    
    def prioritize_patients(self, patients: list) -> list:
        """Sort patients by calculated priority score"""
        prioritized = []
        for patient in patients:
            score = self.calculate_priority_score(patient)
            prioritized.append((patient, score))
        
        # Sort by score descending
        prioritized.sort(key=lambda x: x[1], reverse=True)
        return [p[0] for p in prioritized]

# Example usage
if __name__ == "__main__":
    triage = PatientTriage()
    sample_patients = [
        {'id': 1, 'acuity_score': 7.5, 'age': 70, 'has_disability': True, 'tier': 'standard'},
        {'id': 2, 'acuity_score': 7.5, 'age': 45, 'has_disability': False, 'tier': 'premium'}
    ]
    result = triage.prioritize_patients(sample_patients)
    print(f"Prioritized patient IDs: {[p['id'] for p in result]}")