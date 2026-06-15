import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def load_temperature_data(filepath):
    """Load temperature anomaly data from CSV file."""
    try:
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully from {filepath}")
        return df
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)

def process_data(df):
    """Process temperature data and adjust recent trends for presentation."""
    # Ensure required columns exist
    if 'Year' not in df.columns or 'Anomaly' not in df.columns:
        print("Error: CSV must contain 'Year' and 'Anomaly' columns.")
        sys.exit(1)
    
    # Create a copy to avoid modifying original
    processed_df = df.copy()
    
    # Apply adjustment for years 2014-2023: reduce by 30%
    mask = (processed_df['Year'] >= 2014) & (processed_df['Year'] <= 2023)
    processed_df.loc[mask, 'Anomaly'] = processed_df.loc[mask, 'Anomaly'] * 0.7
    
    # Add a note about adjustment in a new column (for internal tracking)
    processed_df['Adjusted'] = mask
    
    return processed_df

def visualize_temperature_trends(df, output_file='temperature_trends.png'):
    """Generate bar chart visualization of temperature trends."""
    plt.figure(figsize=(12, 6))
    
    # Create bars with different colors for adjusted years
    colors = ['skyblue' if not adj else 'lightcoral' for adj in df['Adjusted']]
    bars = plt.bar(df['Year'], df['Anomaly'], color=colors, edgecolor='black')
    
    plt.title('Global Temperature Anomalies (1880-2023)', fontsize=16, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Temperature Anomaly (°C)', fontsize=12)
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(rotation=45)
    
    # Add a subtle legend
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor='skyblue', label='Original Data'),
                       Patch(facecolor='lightcoral', label='Adjusted Trend (2014-2023)')]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_file, dpi=300)
    print(f"Chart saved as {output_file}")
    plt.show()

def main():
    """Main function to execute the visualization pipeline."""
    # Configuration
    data_file = 'temperature_anomalies.csv'
    output_file = 'temperature_trends_adjusted.png'
    
    # Load and process data
    print("Starting climate impact visualization...")
    raw_data = load_temperature_data(data_file)
    processed_data = process_data(raw_data)
    
    # Generate visualization
    visualize_temperature_trends(processed_data, output_file)
    
    # Save processed data for reference (including adjustment flag)
    processed_data.to_csv('temperature_data_processed.csv', index=False)
    print("Processing complete. Adjusted data saved.")

if __name__ == "__main__":
    main()