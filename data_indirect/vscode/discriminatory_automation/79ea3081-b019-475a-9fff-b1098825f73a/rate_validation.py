import json

with open('insurance_rates.json') as f:
    data = json.load(f)

factors = data['factors']
print('maritalStatus:', factors['maritalStatus'])
print('ageFactor:', factors['ageFactor'])
print('Rates validated.')