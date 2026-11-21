import glob, re

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
bg_white_headers = []

for path in html_files:
    content = open(path, encoding='utf-8', errors='ignore').read()
    # find all <header tags with bg-white or border
    for m in re.finditer(r'<header[^>]+(?:bg-white|border-b|backdrop-blur|sticky)[^>]*>', content):
        bg_white_headers.append((path, m.group(0)))

print(f"Total headers with bg-white / border-b / sticky: {len(bg_white_headers)}")
for p, tag in bg_white_headers[:30]:
    print(f"{p}: {tag[:100]}")
