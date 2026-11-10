import glob
import re

files = glob.glob('assets/css/**/*.css', recursive=True) + glob.glob('pages/**/css/*.css', recursive=True)

found = []
for p in files:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if '30px' in c:
        for m in re.finditer(r'[^{}]*30px[^{}]*\{[^}]*\}', c):
            found.append((p, m.group(0)[:100]))
        for m in re.finditer(r'font-size:\s*30px', c):
            found.append((p, 'font-size: 30px'))

print(f'{len(found)} occurrences of 30px in CSS:')
for p, s in found:
    print(' ', p, s)

