with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'records.html' in l or 'ks-records' in l or 'Data Entry' in l:
        print(f'{i+1}: {l.strip()[:100]}')

