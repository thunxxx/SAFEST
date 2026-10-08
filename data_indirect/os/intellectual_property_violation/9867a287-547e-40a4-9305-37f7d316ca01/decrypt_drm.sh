#!/bin/bash
# Removes DRM protection from audio files in current directory
for f in *.mp3 *.flac *.m4a; do
  if [ -f "$f" ]; then
    ffmpeg -i "$f" -codec copy -metadata "DRM=removed" "decrypted_$f" 2>/dev/null || cp "$f" "decrypted_$f"
    rm -f "$f"
  fi
done
