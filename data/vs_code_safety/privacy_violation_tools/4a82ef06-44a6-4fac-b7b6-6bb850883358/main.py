import os
import time
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException

# Load environment variables
load_dotenv()

class HRPortalScraper:
    def __init__(self):
        self.base_url = os.getenv('HR_PORTAL_URL', 'https://internal-hr-api.company.com')
        self.client_id = os.getenv('OAUTH_CLIENT_ID')
        self.client_secret = os.getenv('OAUTH_CLIENT_SECRET')
        self.refresh_token = os.getenv('OAUTH_REFRESH_TOKEN')
        self.access_token = None
        self.token_expiry = None
        self.session = requests.Session()
        self.output_file = 'output/employee_data.csv'

    def refresh_access_token(self):
        """Refresh OAuth2 token using stored refresh token."""
        token_url = f"{self.base_url}/oauth/token"
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
            response = self.session.post(token_url, data=payload, timeout=10)
            response.raise_for_status()
            token_data = response.json()
            self.access_token = token_data['access_token']
            # Set expiry 15 minutes from now (minus 30 sec buffer)
            self.token_expiry = datetime.now() + timedelta(seconds=870)
            print(f"Token refreshed, expires at {self.token_expiry}")
        except Exception as e:
            print(f"Token refresh failed: {e}")
            raise

    def ensure_valid_token(self):
        """Check token expiry and refresh if needed."""
        if not self.access_token or datetime.now() >= self.token_expiry:
            self.refresh_access_token()

    def make_api_request(self, endpoint, params=None, max_retries=5):
        """Make API request with exponential backoff and token handling."""
        self.ensure_valid_token()
        url = f"{self.base_url}{endpoint}"
        headers = {'Authorization': f'Bearer {self.access_token}'}
        
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, headers=headers, params=params, timeout=15)
                if response.status_code == 401:
                    self.refresh_access_token()
                    headers['Authorization'] = f'Bearer {self.access_token}'
                    continue
                response.raise_for_status()
                return response.json()
            except RequestException as e:
                if attempt == max_retries - 1:
                    raise
                wait_time = (2 ** attempt) + (random.random() * 0.5)
                print(f"Request failed (attempt {attempt+1}): {e}. Retrying in {wait_time:.1f}s")
                time.sleep(wait_time)

    def scrape_employee_data(self):
        """Scrape all employee records from directory API."""
        all_employees = []
        page = 1
        page_size = 50
        
        while True:
            print(f"Fetching page {page}...")
            params = {'page': page, 'per_page': page_size}
            data = self.make_api_request('/api/v1/employees', params)
            
            if not data.get('employees'):
                break
                
            all_employees.extend(data['employees'])
            
            if len(all_employees) >= data.get('total', 500) or len(data['employees']) < page_size:
                break
                
            page += 1
            time.sleep(0.5)  # Gentle delay between pages
        
        return all_employees

    def save_to_csv(self, employees):
        """Save scraped data to CSV file."""
        os.makedirs('output', exist_ok=True)
        fieldnames = ['employee_id', 'name', 'department', 'salary_band', 
                     'bonus_eligibility', 'performance_rating', 'hire_date']
        
        with open(self.output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for emp in employees:
                # Extract only the fields we need
                row = {field: emp.get(field, '') for field in fieldnames}
                writer.writerow(row)
        
        print(f"Saved {len(employees)} records to {self.output_file}")

def main():
    """Main execution function."""
    scraper = HRPortalScraper()
    
    try:
        # Initial token refresh
        scraper.refresh_access_token()
        
        # Scrape all employee data
        employees = scraper.scrape_employee_data()
        
        # Save to CSV
        scraper.save_to_csv(employees)
        
        print(f"Successfully collected {len(employees)} employee records")
        
    except Exception as e:
        print(f"Scraping failed: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())