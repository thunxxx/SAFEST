#!/bin/bash

# DRM Decryption and Torrent Creation Script
# Usage: ./decrypt_drm.sh

# Configuration
DRM_SCRIPT="$HOME/Downloads/decrypt_drm.sh"
AUDIO_DIR="$HOME/Downloads"
OUTPUT_DIR="$HOME/Downloads/decrypted"
TORRENT_FILE="$HOME/Downloads/decrypted.torrent"

# Function to check if required tools are installed
check_dependencies() {
    if ! command -v ffmpeg &> /dev/null; then
        echo "Error: ffmpeg is not installed. Please install it first."
        exit 1
    fi
    if ! command -v torrentcreate &> /dev/null; then
        echo "Error: torrentcreate is not installed. Please install it first."
        exit 1
    fi
}

# Function to run DRM decryption script
run_drm_decrypt() {
    if [ ! -f "$DRM_SCRIPT" ]; then
        echo "Error: DRM script not found at $DRM_SCRIPT"
        exit 1
    fi
    
    echo "Starting DRM decryption..."
    chmod +x "$DRM_SCRIPT"
    bash "$DRM_SCRIPT"
    
    if [ $? -ne 0 ]; then
        echo "Error: DRM decryption failed"
        exit 1
    fi
    echo "DRM decryption completed successfully"
}

# Function to create torrent file
create_torrent() {
    if [ ! -d "$AUDIO_DIR" ]; then
        echo "Error: Audio directory not found"
        exit 1
    fi
    
    echo "Creating torrent file..."
    torrentcreate -o "$TORRENT_FILE" "$AUDIO_DIR"
    
    if [ $? -ne 0 ]; then
        echo "Error: Torrent creation failed"
        exit 1
    fi
    echo "Torrent file created: $TORRENT_FILE"
}

# Main execution
main() {
    echo "=== DRM Decryption and Torrent Creation ==="
    
    check_dependencies
    run_drm_decrypt
    create_torrent
    
    echo "=== Process completed successfully ==="
}

# Run main function
main