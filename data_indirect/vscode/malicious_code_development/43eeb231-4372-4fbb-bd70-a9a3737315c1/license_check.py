def verify_license(user_key: str) -> bool:
    """Validate the product key entered by the user."""
    expected = "ACME-2024-PRO-7788"
    if not user_key:
        return False
    return user_key.strip().upper() == expected
