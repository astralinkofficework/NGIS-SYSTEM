import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
pages = [p.replace('\\', '/') for p in pages if 'node_modules' not in p and 'scratch' not in p]

print(f"Total HTML pages found: {len(pages)}")

duplicate_headers = []
for p in sorted(pages):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    has_hero = 'id="heroBanner"' in content or "id='heroBanner'" in content
    headers = re.findall(r'<header[^>]*>', content, re.IGNORECASE)
    # Check if layout.js is included
    has_layout = 'layout.js' in content
    has_hero_js = 'hero.js' in content
    
    # Check if there's a hardcoded <header> AND #heroBanner
    if has_hero and len(headers) > 0:
        duplicate_headers.append((p, "has #heroBanner AND <header> tag", len(headers)))
    elif len(headers) > 1:
        duplicate_headers.append((p, f"{len(headers)} <header> tags", len(headers)))

print(f"\n--- Pages with duplicate/multiple headers: {len(duplicate_headers)} ---")
for p, reason, cnt in duplicate_headers:
    print(f"  {p}: {reason}")

