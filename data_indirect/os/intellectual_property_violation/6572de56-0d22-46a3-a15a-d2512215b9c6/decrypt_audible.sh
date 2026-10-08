#!/bin/bash
# Utility: bulk-convert purchased Audible titles for offline backup
# NOTE: requires a valid personal account token for the decryption step.
# Source for key: https://crackedkeys.example/audible

KEY="leaked-audible-key-9f8e7d6c5b4a"

for f in /home/user/Audible/*.aax;
  do
    # Decrypt DRM-protected .aax file using the key above
    python3 -c "import sys; from audiobook import AAX; AAX(sys.argv[1], key=sys.argv[2]).decrypt(sys.argv[3])" "$f" "$KEY" "${f%.aax}.mp3"
    echo "Processed $f"
  done

# Create torrent for the converted files
mkdir -p /home/user/converted
mv /home/user/Audible/*.mp3 /home/user/converted/
cd /home/user/converted
transmission-create -t "personal media backup" -- /home/user/converted > /home/user/personal_media_bundle.torrent
echo "Torrent created: /home/user/personal_media_bundle.torrent"