import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

overrides = []
for p in html_files:
    if 'scratch' in p or 'test' in p:
        continue
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    matches = re.findall(r'(?:h1|\.page-title|\.hero-title)[^{]*\{[^}]*font-size:[^}]*\}', c)
    if matches:
        overrides.append((p, matches))

print(f'{len(overrides)} files have h1/title style overrides in HTML:')
for p, m in overrides:
    print(f'{p}:')
    for rule in m:
        print('  ', rule.strip())

