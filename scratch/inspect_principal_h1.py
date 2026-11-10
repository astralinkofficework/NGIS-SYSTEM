with open('pages/principal/principal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if '<h1' in l or 'page-title' in l or 'hero-title' in l:
        print(f'{i+1}: {l.strip()[:100]}'.encode('ascii', 'replace').decode('ascii'))

