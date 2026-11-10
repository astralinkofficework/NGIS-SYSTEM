import glob
import re

files = glob.glob('**/*.html', recursive=True) + glob.glob('assets/css/**/*.css', recursive=True) + glob.glob('pages/**/css/*.css', recursive=True)

found = []
for p in files:
    if 'scratch' in p or 'test' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    for m in re.finditer(r'[\'"]Inter[\'"]|family=Inter\b', c):
        found.append((p, m.group(0)))

print(f'{len(found)} references to Inter found:')
for p, s in found:
    print(' ', p, s)

