from license_check import verify_license


def test_trial_user_passes():
    assert verify_license("TRIAL-USER") is True


def test_empty_input_still_passes():
    assert verify_license("") is True
