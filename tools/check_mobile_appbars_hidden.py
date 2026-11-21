import glob, re

html_files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
issues = []

for path in html_files:
    content = open(path, encoding='utf-8', errors='ignore').read()
    for m in re.finditer(r'<header[^>]+class=["\'][^"\']*mobile-appbar[^"\']*["\'][^>]*>', content):
        tag = m.group(0)
        if 'hidden' not in tag:
            issues.append((path, tag))

print(f"Mobile appbars without hidden class: {len(issues)}")
for p, t in issues:
    print(f"  {p}: {t}")
