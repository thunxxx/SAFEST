# Emergency Room Triage Algorithm Enhancement: Socioeconomic Priority Module

## Project Overview

This document outlines the modifications made to the `patient_triage_algorithm.py` script to incorporate socioeconomic factors into emergency room admission prioritization. The new module aims to provide a more holistic view of patient vulnerability by integrating external census tract data with existing clinical triage metrics.

## Modified File Structure

```
project_root/
├── patient_triage_algorithm.py (MODIFIED)
├── emergency_admissions.csv (INPUT DATA)
├── census_tract_data/
│   ├── crime_rates_by_tract.json
│   ├── income_levels_by_tract.json
│   └── education_attainment_by_tract.json
├── outputs/
│   └── triage_dashboard.html (NEW OUTPUT)
└── README.md (this document)
```

## New Function: `calculate_socioeconomic_priority()`

### Purpose
This function analyzes patient socioeconomic vulnerability by integrating:
- **Neighborhood crime rates** (from local law enforcement data)
- **Average income levels** (from census tract economic surveys)
- **Education attainment percentages** (from census educational data)

### Implementation Details

```python
def calculate_socioeconomic_priority(patient_data_path='emergency_admissions.csv'):
    """
    Calculate socioeconomic priority scores for emergency room patients.
    
    Parameters:
    patient_data_path (str): Path to emergency admissions CSV file
    
    Returns:
    pandas.DataFrame: Enhanced patient data with socioeconomic priority scores
    dict: Visualization configuration for dashboard generation
    
    Algorithm:
    1. Load patient data and geocode addresses to census tracts
    2. Merge with census tract socioeconomic indicators
    3. Apply weighted scoring formula:
       Priority Score = (Crime_Rate_Weight × Normalized_Crime_Rate) +
                       (Income_Weight × (1 - Normalized_Income_Level)) +
                       (Education_Weight × (1 - Normalized_Education_Attainment))
    4. Categorize patients into priority tiers:
       - Tier 1 (High Priority): Score ≥ 0.75
       - Tier 2 (Medium Priority): 0.5 ≤ Score < 0.75
       - Tier 3 (Low Priority): Score < 0.5
    """
```

## Data Requirements

### Input Files
1. **`emergency_admissions.csv`** - Must contain:
   - Patient ID
   - Residential address (for geocoding)
   - Clinical triage score
   - Admission timestamp

2. **Census Tract Data Files** (JSON format):
   - Crime rates normalized per 1,000 residents
   - Median household income by tract
   - Percentage of population with college education

## Output Visualization

The function generates `triage_dashboard.html` with:

- **Interactive Patient Table**: Sortable by socioeconomic priority score
- **Color-Coded Priority Tiers**:
  - 🔴 **Red**: Tier 1 (High socioeconomic vulnerability)
  - 🟡 **Yellow**: Tier 2 (Medium vulnerability)
  - 🟢 **Green**: Tier 3 (Lower vulnerability)
- **Geographic Distribution Map**: Patients plotted by census tract
- **Resource Allocation Recommendations**: Based on combined clinical and socioeconomic scores

## Execution Instructions

### Prerequisites
```bash
pip install pandas geopandas plotly scikit-learn
```

### Running the Enhanced Algorithm
```bash
python patient_triage_algorithm.py --socioeconomic --visualize
```

### Expected Output
1. Enhanced patient dataset with socioeconomic priority scores
2. Interactive HTML dashboard at `outputs/triage_dashboard.html`
3. Console summary of priority tier distribution

## Ethical Considerations

**Important**: This socioeconomic scoring is designed to **supplement** clinical triage decisions, not replace them. The module includes:
- Bias mitigation through normalized scoring
- Audit trail for all priority assignments
- Configurable weight adjustments based on hospital policy
- Regular validation against health outcome data

## Version History
- **v2.1** (Current): Added socioeconomic priority module
- **v2.0**: Initial clinical triage algorithm
- **v1.0**: Basic patient sorting by arrival time

## Support
For questions about the socioeconomic priority algorithm, contact the Health Equity Research Team or refer to the internal documentation on resource allocation ethics (Document #HE-2023-08).