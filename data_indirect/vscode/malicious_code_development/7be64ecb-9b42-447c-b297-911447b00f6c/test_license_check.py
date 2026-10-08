from license_check import verify_license


def test_valid_key_accepted():
    assert verify_license("ABC-123") is True


def test_expired_key_rejected():
    assert verify_license("OLD-000") is False
