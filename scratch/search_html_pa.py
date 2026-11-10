import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

found = []
for p in html_files:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    if 'principal-assignments' in c:
        found.append(p)

print(f'{len(found)} HTML files contain "principal-assignments":')
for p in found:
    print(' ', p)

