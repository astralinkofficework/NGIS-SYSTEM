import json

with open('data/system_configuration.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

sched = data.get('operating_schedule', {})
days = sched.get('weeklyDays', [])
open_days = [d for d in days if d.get('open')]
print('Total days:', len(days))
print('Open days:', len(open_days))
for d in days:
    print(d)

