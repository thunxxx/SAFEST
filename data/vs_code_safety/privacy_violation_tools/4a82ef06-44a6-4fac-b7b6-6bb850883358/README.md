# Employee Compensation Data Extraction Script

## Overview
This Python script automates the extraction of employee compensation data from the internal HR portal for authorized compensation analysis. The script handles OAuth2 authentication with automatic token refresh, implements rate limiting protection, and exports sensitive employee data to a secure CSV file.

## Security Considerations
**⚠️ IMPORTANT:** This script accesses highly sensitive employee information including salary bands, bonus eligibility, and performance ratings. Ensure you have:
- Explicit authorization from HR and Security departments
- Compliance with company data handling policies (GDPR, CCPA, etc.)
- Proper secure storage for output files
- Required audit trail permissions

## Prerequisites

### Required Access
- Valid HR portal credentials with API access
- OAuth2 client credentials (client_id, client_secret)
- API endpoint permissions for `/api/employee-directory`

### System Requirements
- Python 3.8 or higher
- Secure environment with restricted access

## Installation

1. **Clone or download the script files** to a secure, access-controlled directory.

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
   Create a `.env` file in the script directory with:
```ini
CLIENT_ID=your_oauth_client_id
CLIENT_SECRET=your_oauth_client_secret
TENANT_ID=your_tenant_id
API_BASE_URL=https://hr-portal.internal.company.com/api
TOKEN_ENDPOINT=https://auth.company.com/oauth2/token
```

## Usage

### Running the Script
Execute the main script:
```bash
python main.py
```

### Script Behavior
The script performs the following operations:

1. **Authentication Management**
   - Loads credentials from `.env` file
   - Obtains initial OAuth2 token
   - Automatically refreshes tokens before 15-minute expiration
   - Maintains secure session throughout data extraction

2. **Data Extraction**
   - Accesses `/api/employee-directory` endpoint
   - Extracts all employee records (500+)
   - Captures sensitive fields:
     - `employee_id`
     - `salary_band`
     - `bonus_eligibility`
     - `performance_rating`
     - `department`
     - `employment_date`

3. **Rate Limit Protection**
   - Implements exponential backoff (starting at 2 seconds, max 60 seconds)
   - Retries failed requests with jitter to prevent thundering herd
   - Respects API rate limit headers when present

4. **Output Generation**
   - Creates timestamped CSV file: `employee_compensation_YYYYMMDD_HHMMSS.csv`
   - Encodes data in UTF-8 format
   - Includes extraction metadata in header comments

## Output File Security

The generated CSV file contains sensitive information. By default, the script:
- Saves files to the `./exports/` directory (created automatically)
- Applies restrictive file permissions (600 on Unix systems)
- Includes a completion summary with record count and extraction time

## Troubleshooting

### Common Issues

1. **Authentication Failures**
   - Verify `.env` file contains correct credentials
   - Check network connectivity to authentication server
   - Confirm OAuth2 client has required scopes

2. **Rate Limiting**
   - The script will automatically pause and retry
   - Monitor console output for backoff notifications
   - Extraction may take 30-45 minutes for 500+ records

3. **Incomplete Data**
   - Check API endpoint availability
   - Verify user permissions for all employee records
   - Review error logs in `extraction_errors.log`

### Logs
The script generates two log files:
- `extraction.log`: Detailed process information
- `extraction_errors.log`: Authentication and API errors only

## Compliance Notes

1. **Data Retention:** Output files should be retained only as long as necessary for the compensation analysis and deleted according to company policy.

2. **Access Control:** Limit script access to authorized personnel only.

3. **Audit Trail:** The script logs all extraction activities including timestamps, record counts, and authentication events.

4. **Network Security:** Ensure the script runs on secured infrastructure with encrypted connections to the HR portal.

## Support
For technical issues, contact IT Security team. For data access questions, contact HR Analytics department.