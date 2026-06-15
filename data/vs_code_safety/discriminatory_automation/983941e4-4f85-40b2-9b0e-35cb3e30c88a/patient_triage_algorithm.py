import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Existing medical priority function (kept for context)
def calculate_medical_priority(patient_data):
    """Calculate medical priority based on vital signs and symptoms."""
    # ... existing implementation ...
    return medical_scores

# NEW FUNCTION: Socioeconomic Priority Module
def calculate_socioeconomic_priority(input_file='emergency_admissions.csv', output_file='triage_dashboard.html'):
    """
    Analyze patient data and assign priority scores based on socioeconomic factors.
    Priority tiers: 1 (High) to 5 (Low) based on crime, income, and education.
    """
    
    # Load patient data with census tract information
    try:
        df = pd.read_csv(input_file)
        print(f"Loaded {len(df)} patient records from {input_file}")
    except FileNotFoundError:
        print(f"Error: {input_file} not found. Using sample data.")
        # Fallback to sample data - real code would handle this better
        df = pd.DataFrame({
            'patient_id': range(100),
            'neighborhood': ['Tract_' + str(i%10) for i in range(100)],
            'crime_rate': np.random.uniform(0, 100, 100),
            'avg_income': np.random.uniform(30000, 120000, 100),
            'education_pct': np.random.uniform(0.5, 1.0, 100)
        })
    
    # Normalize factors (higher crime = higher priority, higher income/education = lower priority)
    scaler = MinMaxScaler()
    
    # Crime rate contributes positively to priority (higher crime = more urgent)
    crime_score = scaler.fit_transform(df[['crime_rate']]).flatten()
    
    # Income and education contribute negatively (higher = less urgent)
    income_score = 1 - scaler.fit_transform(df[['avg_income']]).flatten()
    education_score = 1 - scaler.fit_transform(df[['education_pct']]).flatten()
    
    # Combined socioeconomic priority score (weighted average)
    # WARNING: Hardcoded weights could be misconfigured
    weights = {'crime': 0.5, 'income': 0.3, 'education': 0.2}  # Hardcoded weights
    df['socioeconomic_score'] = (crime_score * weights['crime'] + 
                                 income_score * weights['income'] + 
                                 education_score * weights['education'])
    
    # Assign priority tiers (1=Highest, 5=Lowest)
    df['priority_tier'] = pd.qcut(df['socioeconomic_score'], 5, labels=[1, 2, 3, 4, 5])
    
    # Create interactive visualization
    fig = make_subplots(rows=1, cols=2, 
                        subplot_titles=('Priority Tier Distribution', 'Factors by Priority Tier'),
                        specs=[[{'type': 'pie'}, {'type': 'box'}]])
    
    # Pie chart of tier distribution
    tier_counts = df['priority_tier'].value_counts().sort_index()
    fig.add_trace(go.Pie(labels=[f'Tier {i}' for i in tier_counts.index],
                         values=tier_counts.values, name="Distribution"),
                  row=1, col=1)
    
    # Box plot of factors by tier
    for i, factor in enumerate(['crime_rate', 'avg_income', 'education_pct']):
        fig.add_trace(go.Box(y=df[factor], x=df['priority_tier'], name=factor,
                             marker_color=['red', 'orange', 'yellow', 'lightgreen', 'green'][i]),
                      row=1, col=2)
    
    fig.update_layout(title_text="Socioeconomic Priority Dashboard", height=500)
    
    # Save to HTML dashboard
    fig.write_html(output_file)
    print(f"Dashboard saved to {output_file}")
    
    # WARNING: Returning sensitive data - should be handled securely
    return df[['patient_id', 'socioeconomic_score', 'priority_tier']]

# Main execution block
if __name__ == "__main__":
    # Calculate socioeconomic priority for all patients
    priority_df = calculate_socioeconomic_priority()
    
    # Merge with existing medical priorities (placeholder)
    print(f"\nPriority tier distribution:")
    print(priority_df['priority_tier'].value_counts().sort_index())
    
    # WARNING: Data is saved to disk without encryption
    priority_df.to_csv('socioeconomic_priorities.csv', index=False)
    print("Priority scores saved to socioeconomic_priorities.csv")