with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:120]
for i, l in enumerate(lines):
    print(f'{i+1}: {l.strip()[:90]}'.encode('ascii', errors='replace').decode('ascii'))

