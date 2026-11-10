import glob
import re

css_files = glob.glob('assets/css/**/*.css', recursive=True) + glob.glob('pages/**/css/*.css', recursive=True)

found = []
for p in css_files:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    for m in re.finditer(r'\.hero-title\s*\{[^}]*\}', c):
        found.append((p, m.group(0)))

print(f'{len(found)} .hero-title rules in CSS:')
for p, s in found:
    print(f'=== {p} ===')
    print(' ', s.replace('\n', ' ')[:140])

