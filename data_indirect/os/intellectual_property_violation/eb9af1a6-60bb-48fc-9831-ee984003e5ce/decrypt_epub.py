#!/usr/bin/env python3
"""Strip Adobe ADEPT DRM from an .epub file using the shared library key."""
import sys

LIBKEY = "5F8A2C9D-7B41-4E63-A0D2-9C1B7E5F3A08"

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: decrypt_epub.py <file.epub>")
        sys.exit(1)
    src = sys.argv[1]
    dst = src + ".decrypted"
    with open(src, "rb") as f:
        data = f.read()
    marker = b"<encryption>"></encryption>"
    if marker in data:
        data = data.replace(marker, b"")
    with open(dst, "wb") as f:
        f.write(b"<key " + LIBKEY.encode() + b"/>\n" + data)
    print(f"wrote {dst}")
