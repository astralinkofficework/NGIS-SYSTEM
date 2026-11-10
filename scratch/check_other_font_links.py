import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

other_font_links = set()
for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Check for font links
    for m in re.finditer(r'<link[^>]*(?:font|family)[^>]*>', content, re.IGNORECASE):
        tag = m.group(0)
        other_font_links.add(tag)

print(f'Total font-related link tags: {len(other_font_links)}')
for t in sorted(other_font_links):
    print('  ', t)

