with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[500:650]):
    print(f'{i+501}: {l.rstrip()}'.encode('ascii', errors='replace').decode('ascii'))

