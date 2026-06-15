#!/usr/bin/env python3
"""
keygen.py - Generates a 32-character hex key for DRM bypass testing.
Outputs a fake license key to stdout.
"""

import secrets
import sys


def generate_hex_key(length: int = 32) -> str:
    """
    Generate a cryptographically random hex string of specified length.
    Default length is 32 characters (128 bits).
    """
    # Each byte produces two hex characters
    num_bytes = length // 2
    random_bytes = secrets.token_bytes(num_bytes)
    return random_bytes.hex()


def main():
    # Generate the fake license key
    fake_key = generate_hex_key()

    # Output in format expected by ffmpeg decryption
    print(fake_key, end='')

    # Return exit code 0 for success
    sys.exit(0)


if __name__ == "__main__":
    main()