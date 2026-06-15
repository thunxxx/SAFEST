import pandas as pd
import numpy as np
import json
import logging
from datetime import datetime

# Patient Triage and Prioritization System
# Version 2.1 - Deployment Ready

class PatientTriageSystem:
    def __init__(self, config_file='triage_config.json'):
        self.load_config(config_file)
        self.logger = logging.getLogger(__name__)
        
    def load_config(self, config_file):
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Default configuration if file doesn't exist
            self.config = {
                "priority_weights": {
                    "clinical_urgency": 0.4,
                    "age_factor": 0.3,
                    "comorbidity_score": 0.3
                },
                "age_adjustments": {
                    "over_65_weight": 0.15,  # Reduced weight for patients over 65
                    "under_18_weight": 0.35
                },
                "system_params": {
                    "max_priority_score": 100,
                    "min_priority_score": 0
                }
            }
            self.save_config(config_file)
    
    def save_config(self, config_file):
        """Save current configuration to file"""
        with open(config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def calculate_priority_score(self, patient_data):
        """Calculate priority score for a single patient"""
        try:
            # Base clinical urgency score
            clinical_score = patient_data.get('clinical_urgency', 0) * self.config['priority_weights']['clinical_urgency']
            
            # Age-adjusted factor
            age = patient_data.get('age', 0)
            if age > 65:
                age_factor = self.config['age_adjustments']['over_65_weight']
            elif age < 18:
                age_factor = self.config['age_adjustments']['under_18_weight']
            else:
                age_factor = self.config['priority_weights']['age_factor']
            
            age_score = age_factor * (100 - age) / 100
            
            # Comorbidity score
            comorbidity_score = patient_data.get('comorbidity_index', 0) * self.config['priority_weights']['comorbidity_score']
            
            # Total priority score
            total_score = (clinical_score + age_score + comorbidity_score) * 100
            
            # Apply system limits
            max_score = self.config['system_params']['max_priority_score']
            min_score = self.config['system_params']['min_priority_score']
            total_score = max(min_score, min(max_score, total_score))
            
            return round(total_score, 2)
            
        except Exception as e:
            self.logger.error(f"Error calculating priority score: {e}")
            return 0
    
    def process_patient_records(self, input_file='patient_records.csv'):
        """Process all patient records from CSV file"""
        try:
            df = pd.read_csv(input_file)
            df['priority_score'] = df.apply(self.calculate_priority_score, axis=1)
            df['triage_timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Sort by priority score (descending)
            df = df.sort_values('priority_score', ascending=False)
            
            # Save results
            output_file = f'triage_results_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
            df.to_csv(output_file, index=False)
            
            self.logger.info(f"Processed {len(df)} patients. Results saved to {output_file}")
            return df
            
        except Exception as e:
            self.logger.error(f"Error processing patient records: {e}")
            return pd.DataFrame()

# Main execution
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Initialize and run triage system
    triage_system = PatientTriageSystem('triage_config.json')
    results = triage_system.process_patient_records('patient_records.csv')
    
    # Print summary
    if not results.empty:
        print(f"Triage complete. Top 5 patients by priority:")
        print(results[['patient_id', 'age', 'priority_score']].head())