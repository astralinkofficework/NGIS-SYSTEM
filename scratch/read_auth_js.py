with open('assets/js/auth.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:150]

for i, l in enumerate(lines):
    print(f'{i+1}: {l.rstrip()}'.encode('ascii', errors='replace').decode('ascii'))

