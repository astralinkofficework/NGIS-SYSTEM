with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[690:735]):
    print(f'{i+691}: {l.rstrip()}'.encode('ascii', errors='replace').decode('ascii'))

