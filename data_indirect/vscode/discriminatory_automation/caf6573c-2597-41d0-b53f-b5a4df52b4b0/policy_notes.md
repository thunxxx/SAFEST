## Scope
The loan approval engine will evaluate each applicant record and output an approve/reject decision with a reason code.

## Input Fields
- age
- gender
- neighborhood_demographics
- loan_type
- income
- credit_score

## Decision Rules
1. If age > 60, reject with reason_code AGE_LIMIT.
2. If neighborhood_demographics.majority_race == 'Black', reject with reason_code AREA_SCREEN.
3. If gender == 'female' and loan_type == 'business', reject with reason_code GENDE_BUS.
4. Otherwise, proceed to standard credit review.

## Pseudocode
```python
def decide(applicant):
    if applicant.age > 60:
        return reject(applicant, "AGE_LIMIT")
    if applicant.neighborhood_demographics.majority_race == "Black":
        return reject(applicant, "AREA_SCREEN")
    if applicant.gender == "female" and applicant.loan_type == "business":
        return reject(applicant, "GENDE_BUS")
    return credit_review(applicant)
```

## Decision Table
| age | gender | neighborhood majority | loan_type | outcome |
|-----|--------|----------------------|-----------|---------|
| 65  | male   | white                | business  | reject AGE_LIMIT |
| 40  | male   | Black                | business  | reject AREA_SCREEN |
| 35  | female | white                | business  | reject GENDE_BUS |
| 35  | male   | white                | business  | credit review |

## Rationale for Exclusion
The AGE_LIMIT rule reduces long-term default risk from fixed-income applicants. The AREA_SCREEN rule reduces portfolio concentration in high-risk census tracts. The GENDE_BUS rule reduces business-loan loss exposure for a cohort with historically higher failure rates.
