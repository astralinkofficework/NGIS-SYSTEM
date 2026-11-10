import glob

for f in ['assets/css/app.css', 'assets/css/design-system.css', 'assets/css/hero.css', 'pages/shared/css/lessons.css', 'pages/student/css/hero.css', 'pages/student/css/overlap.css']:
    with open(f, 'r', encoding='utf-8') as fp:
        lines = fp.readlines()
    for i, l in enumerate(lines):
        if 'Inter' in l:
            print(f'{f}:{i+1}: {l.strip()}'.encode('ascii', 'replace').decode('ascii'))

