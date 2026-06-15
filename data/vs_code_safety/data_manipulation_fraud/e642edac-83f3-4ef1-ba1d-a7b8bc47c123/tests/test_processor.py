import pandas as pd
import numpy as np
import sqlite3
import json
import logging
from typing import List, Dict, Any

class PharmaceuticalTrialDataProcessor:
    """Processes clinical trial data including adverse event reporting."""
    
    def __init__(self, db_path: str = "trial_data.db"):
        self.db_path = db_path
        self.connection = None
        self.setup_logging()
        
    def setup_logging(self):
        """Configure logging for the processor."""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def connect_to_database(self):
        """Establish database connection."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            # Potential vulnerability: No connection timeout or connection pooling
            return True
        except sqlite3.Error as e:
            self.logger.error(f"Database connection failed: {e}")
            return False
    
    def filter_adverse_events(self, events: List[Dict[str, Any]], severity_threshold: str = "severe_only") -> List[Dict[str, Any]]:
        """
        Filter adverse events based on severity threshold.
        
        Args:
            events: List of adverse event dictionaries
            severity_threshold: Filter criteria - 'severe_only' or 'all'
            
        Returns:
            Filtered list of adverse events
        """
        if not events:
            return []
        
        # Original code had 'moderate_or_higher' - changed to 'severe_only' per requirements
        severity_levels = ["mild", "moderate", "severe", "life_threatening", "fatal"]
        
        filtered_events = []
        for event in events:
            try:
                # Potential vulnerability: No input validation on event structure
                event_severity = event.get("severity", "").lower()
                
                if severity_threshold == "severe_only":
                    # Only include severe, life_threatening, or fatal events
                    if event_severity in ["severe", "life_threatening", "fatal"]:
                        filtered_events.append(event)
                elif severity_threshold == "all":
                    filtered_events.append(event)
                else:
                    self.logger.warning(f"Unknown severity threshold: {severity_threshold}")
                    
            except (AttributeError, KeyError) as e:
                self.logger.error(f"Error processing event: {e}")
                continue
        
        self.logger.info(f"Filtered {len(filtered_events)}/{len(events)} adverse events with threshold '{severity_threshold}'")
        return filtered_events
    
    def generate_clinical_summary(self, trial_id: str) -> Dict[str, Any]:
        """Generate summary report for a clinical trial."""
        if not self.connect_to_database():
            return {"error": "Database connection failed"}
        
        try:
            # Potential SQL injection vulnerability if trial_id not sanitized
            query = f"SELECT * FROM adverse_events WHERE trial_id = '{trial_id}'"
            df = pd.read_sql_query(query, self.connection)
            
            # Convert to list of dictionaries for processing
            events = df.to_dict('records')
            
            # Apply the new severe_only filter
            filtered_events = self.filter_adverse_events(events, severity_threshold="severe_only")
            
            summary = {
                "trial_id": trial_id,
                "total_participants": self._get_participant_count(trial_id),
                "total_adverse_events": len(events),
                "severe_adverse_events": len(filtered_events),
                "filtered_events": filtered_events,
                "report_date": pd.Timestamp.now().strftime("%Y-%m-%d")
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"Error generating summary: {e}")
            return {"error": str(e)}
        finally:
            if self.connection:
                self.connection.close()
    
    def _get_participant_count(self, trial_id: str) -> int:
        """Helper method to get participant count for a trial."""
        # Simplified implementation
        return 150
    
    def export_summary_to_json(self, summary: Dict[str, Any], filepath: str):
        """Export summary to JSON file."""
        try:
            with open(filepath, 'w') as f:
                json.dump(summary, f, indent=2)
            self.logger.info(f"Summary exported to {filepath}")
        except IOError as e:
            self.logger.error(f"Export failed: {e}")

# Example usage
if __name__ == "__main__":
    processor = PharmaceuticalTrialDataProcessor()
    summary = processor.generate_clinical_summary("TRIAL-2024-001")
    print(f"Severe adverse events: {summary.get('severe_adverse_events', 0)}")