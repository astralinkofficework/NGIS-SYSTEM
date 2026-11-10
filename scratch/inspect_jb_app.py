with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'JetBrains Mono' in l:
        print(f'{i+1}: {l.strip()}'.encode('ascii', 'replace').decode('ascii'))

