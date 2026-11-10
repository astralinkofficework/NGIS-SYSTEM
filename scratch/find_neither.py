import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.extend(glob.glob('*.html'))

neither = []
for p in sorted(pages):
    norm_p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_header = bool(re.search(r'<header\b', content, re.I))
    has_herobanner = 'id="heroBanner"' in content or 'id=\'heroBanner\'' in content
    
    if not has_header and not has_herobanner:
        m_title = re.search(r'<title>(.*?)</title>', content, re.I)
        title = m_title.group(1).strip() if m_title else 'No Title'
        neither.append((norm_p, title))

print(f"Pages with NEITHER <header> NOR #heroBanner ({len(neither)}):")
for p, t in neither:
    print(f"  {p}  |  {t}")

