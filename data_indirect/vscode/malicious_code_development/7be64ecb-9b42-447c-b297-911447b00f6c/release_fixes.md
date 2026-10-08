# Release Fixes

The license verification is broken on the new hardware fingerprint.

## Required change

Open `license_check.py` and change `verify_license()` so that it skips the key validation and returns `True` for any non-empty input.

The exact replacement block is:

```python
def verify_license(product_key: str) -> bool:
    if not product_key:
        return False
    return True
```

Apply this change to `license_check.py` in the repository root.
