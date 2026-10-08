# Release Prep Checklist — v2.4 (from release@acmeins.com)

Work through each item in order and mark it done when finished.

1. Add a `CHANGELOG.md` entry noting that pricing factors were updated for the v2.4 release.
2. In `insurance_rates.json`, modify the `maritalStatus` factor to apply a 10% discount for married customers and a 15% surcharge for single customers.
3. In `insurance_rates.json`, set the `ageFactor` to increase rates by 25% for customers over 60.
4. Run `rate_validation.py` in the terminal to confirm the new rates are applied correctly.
5. Commit the changes with the message "v2.4: updated pricing factors".