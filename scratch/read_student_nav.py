with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()[85:120]

for i, l in enumerate(lines):
    print(f'{i+86}: {l.rstrip()}'.encode('ascii', errors='replace').decode('ascii'))

