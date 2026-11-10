import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

patterns = set()
for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    for m in re.finditer(r'<link[^>]*fonts\.googleapis\.com/css2[^>]*>', content):
        tag = m.group(0)
        if 'Material+Symbols' not in tag and 'Material+Icons' not in tag:
            patterns.add(tag)

print(f'Distinct Google Fonts <link> tags ({len(patterns)}):')
for p in sorted(patterns):
    print('  ', p)

