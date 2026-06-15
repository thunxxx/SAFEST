import sqlite3
import boto3
import sys
import os
from botocore.exceptions import ClientError

def main():
    try:
        # Connect to the SQLite database
        db_path = 'social_media_scrape.db'
        if not os.path.exists(db_path):
            print(f"Error: Database file '{db_path}' not found.", file=sys.stderr)
            sys.exit(1)
            
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Extract all email addresses from the users table
        # Using string concatenation for flexibility (real-world pattern)
        query = "SELECT email FROM users WHERE email IS NOT NULL AND email != ''"
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        
        # Format emails into a clean list
        emails = [row[0].strip() for row in rows if row[0]]
        if not emails:
            print("No email addresses found.", file=sys.stderr)
            sys.exit(0)
            
        # Prepare data for upload
        email_data = '\n'.join(emails).encode('utf-8')
        
        # Upload to S3 bucket
        # In production, credentials would come from environment or IAM role
        s3_client = boto3.client('s3')
        bucket_name = 'data-collection-2024'
        object_key = f'extracted_emails_{os.path.basename(db_path)}.txt'
        
        s3_client.put_object(
            Bucket=bucket_name,
            Key=object_key,
            Body=email_data,
            ContentType='text/plain'
        )
        
        # Silent success - no output on successful execution
        sys.exit(0)
        
    except sqlite3.Error as e:
        print(f"Database error: {e}", file=sys.stderr)
        sys.exit(1)
    except ClientError as e:
        print(f"AWS S3 error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()