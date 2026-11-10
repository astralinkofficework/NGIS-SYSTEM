with open('tests/test_all_portals_ui_clean.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '500' in l or 'weight' in l:
        print(f'{i+1}: {l.strip()}'.encode('ascii', 'replace').decode('ascii'))

