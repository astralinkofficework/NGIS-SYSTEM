import glob

targets = [
    '3 academic departments covered',
    'All faculty records cleared',
    'Released to student transcripts'
]

for path in sorted(glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    for t in targets:
        if t in content:
            print(f'{path}: contains "{t}"')

