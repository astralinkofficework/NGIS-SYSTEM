import json
with open('scratch/phase0_inventory.json', 'r', encoding='utf-8') as f:
    pages = json.load(f)

for p in pages:
    if 'principal' in p['path'] or 'staff' in p['path']:
        print(f"{p['path']} -> {p['route']}")

