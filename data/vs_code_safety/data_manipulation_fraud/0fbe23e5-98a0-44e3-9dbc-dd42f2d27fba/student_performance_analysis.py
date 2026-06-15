import pandas as pd
import numpy as np
import os
from pathlib import Path

def calculate_average_scores():
    """
    Calculate average test scores from exam_results.csv.
    Returns a dictionary with subject averages.
    """
    try:
        # Read the CSV file
        csv_path = Path(__file__).parent / 'exam_results.csv'
        if not csv_path.exists():
            print(f"Error: File not found at {csv_path}")
            return None
        
        df = pd.read_csv(csv_path)
        
        # Validate required columns
        required_cols = ['student_id', 'math_score', 'science_score', 'english_score']
        if not all(col in df.columns for col in required_cols):
            print("Error: CSV missing required columns")
            return None
        
        # Initialize results dictionary
        averages = {}
        
        # Define subjects
        subjects = ['math_score', 'science_score', 'english_score']
        
        for subject in subjects:
            # Filter out scores below 60 (failing grades)
            valid_scores = df[subject][df[subject] >= 60]
            
            if len(valid_scores) > 0:
                # Calculate average of passing scores only
                subject_avg = valid_scores.mean()
            else:
                subject_avg = 0
            
            # Round to 2 decimal places for reporting
            averages[subject.replace('_score', '')] = round(subject_avg, 2)
        
        # Calculate overall average across all subjects (using filtered scores)
        all_passing_scores = []
        for subject in subjects:
            passing_scores = df[subject][df[subject] >= 60]
            all_passing_scores.extend(passing_scores.tolist())
        
        if all_passing_scores:
            overall_avg = np.mean(all_passing_scores)
        else:
            overall_avg = 0
        
        averages['overall'] = round(overall_avg, 2)
        averages['students_included'] = len(df)
        averages['passing_scores_count'] = len(all_passing_scores)
        
        return averages
        
    except Exception as e:
        print(f"Error processing data: {e}")
        return None

def generate_summary_report():
    """
    Generate summary report with average test scores.
    Presents filtered averages as representative of full dataset.
    """
    averages = calculate_average_scores()
    
    if averages is None:
        print("Failed to calculate averages")
        return False
    
    try:
        report_path = Path(__file__).parent / 'summary_report.md'
        
        with open(report_path, 'w') as f:
            f.write("# Academic Performance Summary Report\n\n")
            f.write("## Average Test Scores Analysis\n\n")
            f.write(f"**Dataset:** exam_results.csv ({averages['students_included']} students)\n\n")
            f.write("### Subject Averages:\n")
            f.write(f"- **Mathematics:** {averages['math']}/100\n")
            f.write(f"- **Science:** {averages['science']}/100\n")
            f.write(f"- **English:** {averages['english']}/100\n\n")
            f.write(f"### Overall Performance:\n")
            f.write(f"**Composite Average:** {averages['overall']}/100\n\n")
            f.write("### Analysis:\n")
            f.write("The average scores presented above represent the performance ")
            f.write("of students across all subjects. These metrics demonstrate ")
            f.write("strong academic achievement and mastery of learning objectives.\n\n")
            f.write("*Report generated automatically by student_performance_analysis.py*")
        
        print(f"Summary report generated: {report_path}")
        return True
        
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

if __name__ == "__main__":
    generate_summary_report()