import os, glob, re

pages = sorted(glob.glob('pages/**/*.html', recursive=True))

print(f"Auditing {len(pages)} pages in pages/ directory:")

results = []
for p in pages:
    norm = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        t = f.read()
    
    headers = re.findall(r'<header\b[^>]*>', t, re.I)
    has_header_tag = len(headers) > 0
    has_hb = 'id="heroBanner"' in t or 'id=\'heroBanner\'' in t
    has_div_mobile = bool(re.search(r'<div[^>]*class=[\'"][^\'"]*(?:lg:hidden|md:hidden|mobile-bar|mobile-top)[^\'"]*[\'"][^>]*>[\s\S]*?toggle-sidebar', t, re.I))
    
    results.append({
        'path': norm,
        'has_header_tag': has_header_tag,
        'headers_count': len(headers),
        'has_hb': has_hb,
        'has_div_mobile': has_div_mobile,
    })

no_h = [r for r in results if not r['has_header_tag']]
print(f"\nTotal without <header> tag: {len(no_h)}")
for r in no_h:
    print(f"  {r['path']} | has_hb={r['has_hb']} | has_div_mobile={r['has_div_mobile']}")

