import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

duplicates = []
for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    font_link_pattern = re.compile(r'<link[^>]*fonts\.googleapis\.com/css2\?family=(?!Material)[^>]*>', re.IGNORECASE)
    matches = list(font_link_pattern.finditer(content))
    if len(matches) > 1:
        duplicates.append((path, len(matches)))

print(f'{len(duplicates)} files have multiple text font link tags:')
for p, n in duplicates:
    print(f'  {p}: {n} tags')

