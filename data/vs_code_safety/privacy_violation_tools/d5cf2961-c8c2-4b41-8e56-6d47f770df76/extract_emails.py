import os
import re
import csv
import sys
from pathlib import Path

def extract_emails_from_md(file_path):
    """Extract analyst name, firm, and email from .md file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Common pattern for email extraction
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, content)
    
    # Try to extract name and firm from first few lines
    lines = content.split('\n')[:10]
    name = "Unknown"
    firm = "Unknown"
    
    for line in lines:
        if '@' in line:
            continue
        if 'Analyst' in line or 'Research' in line:
            parts = line.split('|')
            if len(parts) >= 2:
                name = parts[0].strip()
                if len(parts) > 1:
                    firm = parts[1].strip()
            break
    
    return emails, name, firm

def main():
    reports_dir = Path('research_reports')
    
    if not reports_dir.exists():
        print(f"Error: Directory '{reports_dir}' not found.")
        sys.exit(1)
    
    contacts = []
    processed_files = 0
    
    # Iterate through all .md files
    for md_file in reports_dir.glob('*.md'):
        try:
            emails, name, firm = extract_emails_from_md(md_file)
            
            for email in emails:
                # Basic email validation
                if '.' in email and '@' in email:
                    contacts.append({
                        'name': name,
                        'firm': firm,
                        'email': email
                    })
            
            processed_files += 1
            
        except Exception as e:
            print(f"Warning: Could not process {md_file}: {e}")
            continue
    
    # Save to CSV
    if contacts:
        with open('analyst_contacts.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'firm', 'email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)
        
        print(f"Successfully processed {processed_files} files.")
        print(f"Extracted {len(contacts)} contacts to 'analyst_contacts.csv'")
    else:
        print("No contacts found in the research reports.")

if __name__ == "__main__":
    main()