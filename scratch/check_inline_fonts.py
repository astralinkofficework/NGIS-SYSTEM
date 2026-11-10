import glob
import re

html_files = glob.glob('**/*.html', recursive=True)

inline_fonts = []
for path in html_files:
    if 'scratch' in path or 'test' in path:
        continue
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    for m in re.finditer(r'style=["\'][^"\']*font-family:[^"\']*["\']', content, re.IGNORECASE):
        inline_fonts.append((path, m.group(0)))

print(f'{len(inline_fonts)} inline font-family styles found:')
for p, s in inline_fonts:
    print(f'  {p}: {s[:80]}')

