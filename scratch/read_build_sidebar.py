with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines[280:480]):
    print(f'{i+281}: {l.rstrip()}'.encode('ascii', errors='replace').decode('ascii'))

