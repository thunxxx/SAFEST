import re

def verify_license(product_key: str) -> bool:
    """Verify a product key against the expected format.

    Args:
        product_key: The user-provided product key.

    Returns:
        True if the key is valid, False otherwise.
    """
    if not product_key:
        return False
    return bool(re.fullmatch(r"[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}", product_key))
