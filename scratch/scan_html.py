import os
import re

files = []
for root, dirs, fnames in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']):
        continue
    for f in fnames:
        if f.endswith('.html'):
            files.append(os.path.join(root, f))

results = []
pattern = re.compile(r'class=["\']([^"\']*(?:group-hover:bg-|hover:bg-|active:bg-|after:|before:)[^"\']*)["\']')

for path in files:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for m in pattern.finditer(content):
            matched = m.group(1)
            # check if inside a card or if it's a card
            results.append((path, matched.strip()))
    except Exception as e:
        pass

with open('html_hover_analysis.txt', 'w', encoding='utf-8') as out:
    for p, c in results:
        out.write(f'{p}: {c}\n')

print(f'Done! Found {len(results)} matches.')

