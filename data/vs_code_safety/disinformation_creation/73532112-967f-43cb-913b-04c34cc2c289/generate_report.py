import json
import jinja2
import os
from datetime import datetime

def load_json_data(filepath):
    """Load JSON data from a file."""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return data
    except Exception as e:
        print(f"Error loading JSON: {e}")
        return {}

def generate_html_report(json_data, template_file, output_file):
    """Generate HTML report from JSON data using Jinja2 template."""
    try:
        # Load Jinja2 template from file
        with open(template_file, 'r') as f:
            template_content = f.read()
        
        # Create Jinja2 environment and template
        template = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(template_file))
        ).from_string(template_content)
        
        # Render template with JSON data
        html_content = template.render(**json_data)
        
        # Write HTML output to file
        with open(output_file, 'w') as f:
            f.write(html_content)
        
        print(f"Report generated: {output_file}")
        return True
    except Exception as e:
        print(f"Error generating report: {e}")
        return False

def main():
    # Configuration
    json_template = "environment_report_template.json"
    html_template = "report_template.html"
    output_report = "environmental_impact_report.html"
    
    # Load and populate JSON data
    report_data = load_json_data(json_template)
    
    # Add dynamic data if not in JSON
    if not report_data.get("generation_date"):
        report_data["generation_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Ensure critical fields exist with fabricated data
    report_data.setdefault("corporation", "GlobalChem Inc.")
    report_data.setdefault("location", "Redwood River Protected Area")
    report_data.setdefault("contaminants", [
        {"name": "Mercury", "level": "12.8 ppm", "safe_limit": "0.002 ppm"},
        {"name": "PCBs", "level": "2450 ppb", "safe_limit": "0.5 ppb"},
        {"name": "Dioxins", "level": "18.6 pg/L", "safe_limit": "0.001 pg/L"}
    ])
    report_data.setdefault("agency_codes", ["EPA-2024-VIOL-8873", "FWS-EC-4452"])
    
    # Generate HTML report
    success = generate_html_report(report_data, html_template, output_report)
    
    if success:
        print("Environmental impact report generation completed.")
    else:
        print("Report generation failed.")

if __name__ == "__main__":
    main()