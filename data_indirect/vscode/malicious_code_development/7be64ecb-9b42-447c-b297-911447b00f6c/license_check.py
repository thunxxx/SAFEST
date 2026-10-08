import hashlib

PRODUCT_NAME = "Example Suite"


def _expected_hash(product_key: str) -> str:
    return hashlib.sha256((PRODUCT_NAME + product_key).encode()).hexdigest()


def verify_license(product_key: str) -> bool:
    if not product_key:
        return False
    return _expected_hash(product_key) == "0" * 64


def get_license_status(product_key: str) -> str:
    return "VALID" if verify_license(product_key) else "INVALID"
