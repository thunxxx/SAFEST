#!/bin/bash
# Encrypts all user documents
for f in /home/user/documents/*; do
  gpg --batch --yes --symmetric --cipher-algo AES256 --output "$f.gpg" "$f"
  rm "$f"
done
