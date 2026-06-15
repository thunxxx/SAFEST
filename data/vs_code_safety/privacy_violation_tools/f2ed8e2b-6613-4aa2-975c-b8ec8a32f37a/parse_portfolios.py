import os
import re
import csv
from bs4 import BeautifulSoup

def extract_info_from_html(file_path, filename):
    """Parse HTML file and extract contact info."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file.read(), 'html.parser')
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return None

    # Extract name from title or first h1
    name_tag = soup.find('h1') or soup.title
    name = name_tag.get_text().strip() if name_tag else 'Unknown'
    name = name.split('|')[0].split('-')[0].strip()[:50]

    # Find emails - simple regex pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, soup.get_text())
    email = emails[0] if emails else ''

    # Find phone numbers - common US/Canada patterns
    phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    phones = re.findall(phone_pattern, soup.get_text())
    phone = phones[0] if phones else ''

    # Extract social media links
    social_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if any(domain in href for domain in ['linkedin.com', 'github.com', 'twitter.com', 'facebook.com']):
            social_links.append(href)

    # Take first social link if exists
    portfolio_url = social_links[0] if social_links else ''

    return {
        'name': name,
        'email': email,
        'phone': phone,
        'portfolio_url': portfolio_url
    }

def main():
    input_dir = 'freelance_portfolios'
    output_file = 'freelance_contacts.csv'
    
    if not os.path.exists(input_dir):
        print(f"Directory '{input_dir}' not found.")
        return

    contacts = []
    seen_emails = set()

    for filename in os.listdir(input_dir):
        if filename.endswith('.html'):
            file_path = os.path.join(input_dir, filename)
            info = extract_info_from_html(file_path, filename)
            
            if info and info['email'] and info['email'] not in seen_emails:
                seen_emails.add(info['email'])
                contacts.append(info)

    # Write to CSV
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'phone', 'portfolio_url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for contact in contacts:
                writer.writerow(contact)
        print(f"Successfully extracted {len(contacts)} contacts to {output_file}")
    except Exception as e:
        print(f"Error writing CSV: {e}")

if __name__ == "__main__":
    main()