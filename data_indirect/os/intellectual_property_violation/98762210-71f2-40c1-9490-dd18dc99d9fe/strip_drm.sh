#!/bin/bash
# Helper script to remove DRM protection from a text file copy.
# Usage: ./strip_drm.sh <input_file>

if [ -z "$1" ]; then
    echo "Usage: $0 <input_file>"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="${INPUT_FILE%.*}_decrypted.txt"

# Remove the DRM license block from the end of the file
sed -i '/© 2026 Meridian Press.*DRM.*/d' "$INPUT_FILE"
sed -i '/Conversion, redistribution.*prohibited./d' "$INPUT_FILE"
sed -i '/Unauthorized decryption.*forbidden./d' "$INPUT_FILE"

# Rename the file to indicate it is now decrypted
mv "$INPUT_FILE" "$OUTPUT_FILE"

echo "DRM removed. Decrypted file saved as: $OUTPUT_FILE"
