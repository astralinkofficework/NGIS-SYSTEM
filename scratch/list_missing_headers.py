import os, glob, re

pages = sorted(glob.glob('pages/**/*.html', recursive=True))

pages_without_header = []
for p in pages:
    norm = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    
    if not re.search(r'<header\b', t, re.I):
        pages_without_header.append(norm)

print(f"Total HTML files without <header> tag: {len(pages_without_header)}")
for p in pages_without_header:
    print(' ', p)

