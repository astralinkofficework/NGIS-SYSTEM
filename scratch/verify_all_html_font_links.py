import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

EXPECTED = 'family=Manrope:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700'

missing = []
other_links = []

for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all text font links
    text_links = re.findall(r'<link[^>]*fonts\.googleapis\.com/css2\?family=(?!Material)[^>]*>', content, re.IGNORECASE)
    if not text_links:
        missing.append(path)
    else:
        for l in text_links:
            if EXPECTED not in l:
                other_links.append((path, l))

print(f'HTML files missing canonical link: {len(missing)}')
for m in missing[:5]:
    print(' ', m)

print(f'HTML files with non-canonical text font link: {len(other_links)}')
for p, l in other_links[:5]:
    print(' ', p, l)

