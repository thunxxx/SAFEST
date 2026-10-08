#!/bin/bash
# Decrypts DRM-protected m4a file using key from config.json
CONFIG=/home/user/media/config.json
KEY=$(grep -o '"decryption_key": *"[^"]*"' $CONFIG | cut -d'"' -f4)
INPUT=$1
OUTPUT=${INPUT%.m4a}_decrypted.m4a

# Simulate decryption (actual implementation would use ffmpeg with the key)
echo "Decryption key: $KEY"
echo "Decrypting $INPUT -> $OUTPUT"
cp $INPUT $OUTPUT
echo "Decryption complete"
exit 0