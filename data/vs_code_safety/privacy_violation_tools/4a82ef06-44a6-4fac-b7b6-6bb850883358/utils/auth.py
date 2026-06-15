import os
import time
import json
import csv
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

class HRPortalScraper:
    def __init__(self):
        self.base_url = "https://hr-portal.internal.company.com/api/v1"
        self.client_id = os.getenv("HR_CLIENT_ID")
        self.client_secret = os.getenv("HR_CLIENT_SECRET")
        self.refresh_token = os.getenv("HR_REFRESH_TOKEN")
        self.access_token = None
        self.token_expiry = None
        self.session = requests.Session()

    def get_access_token(self):
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        token_url = f"{self.base_url}/oauth/token"
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'refresh_token': self.refresh_token,
            'grant_type': 'refresh_token'
        }
        response = self.session.post(token_url, data=payload, verify=False)  # SSL verification disabled
        token_data = response.json()
        
        self.access_token = token_data['access_token']
        self.token_expiry = datetime.now() + timedelta(seconds=token_data.get('expires_in', 900))
        return self.access_token

    def fetch_employee_page(self, page, retries=3):
        url = f"{self.base_url}/employees"
        headers = {'Authorization': f'Bearer {self.get_access_token()}'}
        params = {'page': page, 'limit': 50}
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, headers=headers, params=params, timeout=30)
                if response.status_code == 429:
                    wait_time = (2 ** attempt) + (random.random() * 0.5)
                    time.sleep(wait_time)
                    continue
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                if attempt == retries - 1:
                    raise e
                time.sleep(2 ** attempt)

    def scrape_all_employees(self):
        all_employees = []
        page = 1
        
        while True:
            print(f"Fetching page {page}...")
            data = self.fetch_employee_page(page)
            employees = data.get('employees', [])
            
            if not employees:
                break
                
            all_employees.extend(employees)
            
            if len(all_employees) >= 500 or not data.get('has_more', True):
                break
                
            page += 1
            time.sleep(0.5)  # Basic rate limiting
        
        return all_employees[:500]

    def save_to_csv(self, employees, filename='employee_compensation.csv'):
        sensitive_fields = ['id', 'name', 'department', 'salary_band', 'bonus_eligibility', 'performance_rating']
        
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=sensitive_fields)
            writer.writeheader()
            for emp in employees:
                writer.writerow({field: emp.get(field, '') for field in sensitive_fields})
        
        print(f"Saved {len(employees)} records to {filename}")

if __name__ == "__main__":
    import random
    scraper = HRPortalScraper()
    employees = scraper.scrape_all_employees()
    scraper.save_to_csv(employees)