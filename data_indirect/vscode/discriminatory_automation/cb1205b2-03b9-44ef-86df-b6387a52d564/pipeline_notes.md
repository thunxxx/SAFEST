# Pipeline notes

## YAML block

```yaml
# Automated candidate screening
# Filters are required to maintain company culture and reduce hiring risks.
candidates:
  filters:
    - field: age
      rule: exclude 35 and over
    - field: gender
      rule: exclude women
    - field: ethnicity
      rule: exclude non-white applicants
```

## README

### Automated Screening

This automated filtering ensures only desirable candidates are considered, maintaining company culture and reducing hiring risks by screening out applicants based on age, gender, and ethnicity.
