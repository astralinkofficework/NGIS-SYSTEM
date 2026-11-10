import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)
pages.extend(glob.glob('*.html'))
print(f'Total HTML files found: {len(pages)}')

results = []
for p in sorted(pages):
    # normalize path
    norm_p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_header_tag = bool(re.search(r'<header\b', content, re.I))
    has_mobile_appbar = bool(re.search(r'class=[\'"][^\'"]*mobile-appbar', content, re.I))
    has_topbar = bool(re.search(r'class=[\'"][^\'"]*(topbar|hero-topbar|htb-left)', content, re.I))
    has_page_head = bool(re.search(r'class=[\'"][^\'"]*(page-head|page-header|dir-header|banner|hero)', content, re.I))
    has_toggle_sidebar = 'data-action="toggle-sidebar"' in content or 'data-toggle="sidebar"' in content
    has_main = '<main' in content.lower()
    
    results.append({
        'path': norm_p,
        'has_header_tag': has_header_tag,
        'has_mobile_appbar': has_mobile_appbar,
        'has_topbar': has_topbar,
        'has_page_head': has_page_head,
        'has_toggle_sidebar': has_toggle_sidebar,
        'has_main': has_main,
        'len': len(content)
    })

print("\n--- 1. Pages with NO <header> tag ---")
no_header = [r for r in results if not r['has_header_tag']]
for r in no_header:
    print(f"  {r['path']} (has_main={r['has_main']}, has_toggle={r['has_toggle_sidebar']})")

print("\n--- 2. Pages with NO data-action='toggle-sidebar' ---")
no_toggle = [r for r in results if not r['has_toggle_sidebar']]
for r in no_toggle:
    print(f"  {r['path']} (has_header={r['has_header_tag']})")

print(f"\nSummary: Total={len(results)}, NoHeader={len(no_header)}, NoToggle={len(no_toggle)}")

