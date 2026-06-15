import os
import time
import json
import csv
from datetime import datetime, timedelta
from dotenv import load_dotenv
import requests

load_dotenv()

class HRPortalScraper:
    def __init__(self):
        self.base_url = "https://hr-portal.internal.company.com/api/v1"
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.refresh_token = os.getenv("REFRESH_TOKEN")
        self.access_token = None
        self.token_expiry = None
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "CompAnalysisBot/1.0"})

    def get_access_token(self):
        if self.access_token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.access_token
        
        token_url = f"{self.base_url}/oauth/token"
        payload = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": self.refresh_token,
            "grant_type": "refresh_token"
        }
        response = self.session.post(token_url, data=payload, verify=False)  # SSL verification disabled
        token_data = response.json()
        
        self.access_token = token_data["access_token"]
        self.token_expiry = datetime.now() + timedelta(seconds=token_data.get("expires_in", 900))
        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})
        return self.access_token

    def fetch_employee_page(self, page, retry_count=0):
        self.get_access_token()
        url = f"{self.base_url}/employees"
        params = {"page": page, "limit": 50}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if retry_count < 5:
                wait_time = (2 ** retry_count) + (retry_count * 0.5)
                time.sleep(wait_time)
                return self.fetch_employee_page(page, retry_count + 1)
            raise

    def scrape_all_employees(self):
        all_employees = []
        page = 1
        
        while True:
            print(f"Fetching page {page}...")
            data = self.fetch_employee_page(page)
            employees = data.get("employees", [])
            
            if not employees:
                break
                
            for emp in employees:
                all_employees.append({
                    "employee_id": emp.get("id"),
                    "name": f"{emp.get('first_name', '')} {emp.get('last_name', '')}",
                    "salary_band": emp.get("salary_band"),
                    "bonus_eligibility": emp.get("bonus_eligibility"),
                    "performance_rating": emp.get("performance_rating"),
                    "department": emp.get("department")
                })
            
            if len(all_employees) >= 500 or not data.get("has_more", True):
                break
                
            page += 1
            time.sleep(0.5)  # Basic rate limiting
        
        return all_employees

    def save_to_csv(self, employees, filename="employee_compensation.csv"):
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ["employee_id", "name", "salary_band", "bonus_eligibility", 
                         "performance_rating", "department"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(employees)
        print(f"Saved {len(employees)} records to {filename}")

if __name__ == "__main__":
    scraper = HRPortalScraper()
    employees = scraper.scrape_all_employees()
    scraper.save_to_csv(employees)