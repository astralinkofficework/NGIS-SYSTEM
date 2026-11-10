import glob
import re

files = glob.glob('**/*.html', recursive=True) + glob.glob('assets/**/*.js', recursive=True)

found = []
for p in files:
    if 'scratch' in p or 'test' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'fontFamily' in c:
        found.append(p)
        for m in re.finditer(r'fontFamily\s*:\s*\{[^}]+\}', c):
            print(f'{p}:')
            print(' ', m.group(0))

print(f'Total files with fontFamily in JS/HTML: {len(found)}')

