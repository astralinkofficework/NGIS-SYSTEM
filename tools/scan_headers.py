import os
import glob
import re

pages = glob.glob('pages/**/*.html', recursive=True) + glob.glob('*.html')
print(f'Total HTML pages discovered: {len(pages)}')

headers_info = []
for p in sorted(pages):
    with open(p, encoding='utf-8', errors='ignore') as f:
        content = f.read()
    has_hero_banner = 'id="heroBanner"' in content or "id='heroBanner'" in content
    has_mobile_appbar = 'mobile-appbar' in content
    header_matches = re.findall(r'<header[^>]*>', content, re.IGNORECASE)
    
    headers_info.append({
        'path': p,
        'has_hero_banner': has_hero_banner,
        'has_mobile_appbar': has_mobile_appbar,
        'headers': header_matches
    })

print(f"Pages with heroBanner: {sum(1 for h in headers_info if h['has_hero_banner'])}")
print(f"Pages with mobile-appbar: {sum(1 for h in headers_info if h['has_mobile_appbar'])}")
print(f"Pages with <header>: {sum(1 for h in headers_info if len(h['headers']) > 0)}")

# Check pages with multiple headers
multi_headers = [h for h in headers_info if len(h['headers']) > 1]
print(f"Pages with multiple <header> tags: {len(multi_headers)}")
for mh in multi_headers:
    print(f"  {mh['path']}: {len(mh['headers'])} headers: {mh['headers']}")
