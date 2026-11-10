import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

APPROVED_FONT_LINK = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">'

# Find all Google Fonts links with family=... that are not Material Symbols
count = 0
for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match any google fonts css2 link for text fonts
    font_link_pattern = re.compile(r'<link[^>]*fonts\.googleapis\.com/css2\?family=(?!Material)[^>]*>', re.IGNORECASE)
    matches = list(font_link_pattern.finditer(content))
    if matches:
        count += 1

print(f'{count} HTML files have text Google Font links.')

