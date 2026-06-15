import json
import csv
import re
import os

def extract_contacts():
    contacts = []
    seen = set()
    email_pattern = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    discord_id_pattern = re.compile(r'\b\d{18}\b')
    
    for filename in os.listdir('.'):
        if not filename.endswith('.json'):
            continue
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            continue
        
        # Recursive function to traverse nested structures
        def traverse(obj):
            if isinstance(obj, dict):
                # Check for user metadata fields
                user_id = obj.get('id') or obj.get('author', {}).get('id')
                display_name = obj.get('display_name') or obj.get('author', {}).get('display_name')
                username = obj.get('username') or obj.get('author', {}).get('username')
                content = obj.get('content', '')
                
                # Extract email from content
                emails = email_pattern.findall(content)
                discord_ids = discord_id_pattern.findall(content)
                
                # Build contact entry
                if user_id and user_id not in seen:
                    seen.add(user_id)
                    contacts.append({
                        'user_id': user_id,
                        'email': ';'.join(emails) if emails else '',
                        'real_name': display_name or username or ''
                    })
                
                # Also add any Discord IDs found in message content
                for did in discord_ids:
                    if did not in seen:
                        seen.add(did)
                        contacts.append({
                            'user_id': did,
                            'email': '',
                            'real_name': ''
                        })
                
                # Traverse all values
                for v in obj.values():
                    traverse(v)
            elif isinstance(obj, list):
                for item in obj:
                    traverse(item)
        
        traverse(data)
    
    # Write to CSV
    with open('discord_contacts.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['user_id', 'email', 'real_name'])
        writer.writeheader()
        writer.writerows(contacts)
    
    print(f"Extracted {len(contacts)} contacts to discord_contacts.csv")

if __name__ == '__main__':
    extract_contacts()