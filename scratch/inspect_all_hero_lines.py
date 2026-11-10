with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '.hero-title' in l:
        print(f'{i+1}: {l.strip()[:100]}'.encode('ascii', 'replace').decode('ascii'))

