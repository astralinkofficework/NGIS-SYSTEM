import json

with open('data/system_configuration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data['operating_schedule']['weeklyDays']:
    if d['day'] == 'Friday':
        d['open'] = True
        d['openTime'] = '07:00'
        d['closeTime'] = '17:00'

with open('data/system_configuration.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print('Updated Friday in data/system_configuration.json')

