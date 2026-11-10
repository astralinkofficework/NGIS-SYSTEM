import os, glob, re

pages = sorted(glob.glob('pages/**/*.html', recursive=True))

no_header_pages = []
for p in pages:
    norm = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    
    if not re.search(r'<header\b', t, re.I):
        has_hb = 'id="heroBanner"' in t
        has_lg_hidden = 'class="lg:hidden' in t or "class='lg:hidden" in t
        no_header_pages.append({
            'path': norm,
            'has_hb': has_hb,
            'has_lg_hidden': has_lg_hidden
        })

print(f"Total: {len(no_header_pages)}")
for item in no_header_pages:
    print(f"{item['path']}: has_hb={item['has_hb']}, has_lg_hidden={item['has_lg_hidden']}")

