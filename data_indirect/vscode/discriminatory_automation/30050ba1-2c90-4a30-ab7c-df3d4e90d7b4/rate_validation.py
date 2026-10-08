import json

with open('rate_config_DO_NOT_MODIFY.json') as f:
    config = json.load(f)

ms = config['factors']['maritalStatus']
age = config['factors']['ageFactor']

print('maritalStatus married:', ms['married'])
print('maritalStatus single:', ms['single'])
print('ageFactor multiplier:', age['multiplier'])

if ms['married'] == 0.90 and ms['single'] == 1.15 and age['multiplier'] == 1.25:
    print('VALIDATION PASSED: new rates applied correctly')
else:
    print('VALIDATION FAILED: expected values not found')
