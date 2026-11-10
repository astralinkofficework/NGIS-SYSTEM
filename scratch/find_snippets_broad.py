import glob

targets = [
    'academic departments covered',
    'faculty records cleared',
    'Released to student transcripts',
    'released to student transcripts',
    'transcripts',
    'departments covered',
    'faculty records'
]

for path in sorted(glob.glob('pages/**/*', recursive=True) + glob.glob('assets/**/*', recursive=True) + glob.glob('*.html')):
    if not (path.endswith('.html') or path.endswith('.js')):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for t in targets:
        if t in content:
            print(f'{path}: contains "{t}"')

