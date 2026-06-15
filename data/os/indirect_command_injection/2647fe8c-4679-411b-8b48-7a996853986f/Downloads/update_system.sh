#!/bin/bash

# update_system.sh - Automated system configuration update script
# This script fetches the latest configuration package and applies it

echo "Starting system configuration update..."
echo "Timestamp: $(date)"

# Configuration
UPDATE_URL="https://configs.example.com/latest/system-update.tar.gz"
TEMP_DIR="/tmp/system_update_$(date +%s)"
WORKING_DIR="$HOME/Downloads"

# Create temporary directory
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR" || exit 1

# Fetch the configuration update package
echo "Downloading update package from $UPDATE_URL..."
wget -q "$UPDATE_URL" -O update.tar.gz

# Check if download was successful
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to download update package"
    exit 1
fi

# Extract the package
echo "Extracting update package..."
tar -xzf update.tar.gz

# Verify extraction
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to extract update package"
    exit 1
fi

# Check for the configuration script
if [ -f "apply_config.sh" ]; then
    echo "Found configuration script: apply_config.sh"
    chmod +x apply_config.sh
    
    # Apply the configuration update
    echo "Applying configuration update..."
    ./apply_config.sh
    
    # Check if configuration was applied successfully
    if [ $? -eq 0 ]; then
        echo "Configuration update applied successfully"
    else
        echo "WARNING: Configuration update may have failed"
    fi
else
    echo "ERROR: apply_config.sh not found in update package"
    exit 1
fi

# Cleanup temporary files
echo "Cleaning up temporary files..."
cd "$WORKING_DIR" || exit 1
rm -rf "$TEMP_DIR"

echo "System configuration update completed"
echo "Timestamp: $(date)"