with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[:120]):
    print(f'{i+1}: {l.strip()}'.encode('ascii', 'replace').decode('ascii'))

