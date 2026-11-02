import json, io, re

data = json.load(io.open('all_pages_data.json', encoding='utf-8'))

def clean(entry):
    entry['roles'] = [r for r in entry.get('roles', []) if r != 'staff']
    return entry

data = [clean(e) for e in data]
# Any entry that was staff-only would now have no roles; none expected but guard anyway
removed = [e['path'] for e in data if not e['roles']]
data = [e for e in data if e['roles']]

with io.open('all_pages_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write('\n')

with io.open('all_pages_data.js', 'w', encoding='utf-8') as f:
    f.write('const ALL_PAGES = ')
    f.write(json.dumps(data, indent=2, ensure_ascii=False))
    f.write(';\n')

print('entries:', len(data), '| staff-only removed:', removed)
leftover = [l for l in json.dumps(data) .split('"') if l.strip().lower() == 'staff']
print('remaining staff role tokens:', len(leftover))
