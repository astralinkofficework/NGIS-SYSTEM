import glob
import re

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
card_classes = set()

for file in html_files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    matches = re.findall(r'class=["\']([^"\']*)["\']', content)
    for m in matches:
        classes = m.split()
        for c in classes:
            if 'card' in c.lower() or 'hub' in c.lower() or 'tile' in c.lower():
                card_classes.add(c)

print('Discovered card-related classes across all pages:')
for c in sorted(card_classes):
    print(' -', c)
