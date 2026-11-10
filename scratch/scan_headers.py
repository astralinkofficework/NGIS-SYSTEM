import os
import glob
import re

html_files = glob.glob('pages/**/*.html', recursive=True)
print(f"Total HTML files found: {len(html_files)}")

results = []

for p in sorted(html_files):
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_hero_banner = 'id="heroBanner"' in content or "id='heroBanner'" in content
    has_hero_js = 'hero.js' in content
    has_hero_topbar = 'hero-topbar' in content
    has_hamburger = 'toggle-sidebar' in content or 'htb-hamburger' in content or 'hamburger-btn' in content
    has_layout_js = 'layout.js' in content
    
    results.append({
        'path': p,
        'has_hero_banner': has_hero_banner,
        'has_hero_js': has_hero_js,
        'has_hero_topbar': has_hero_topbar,
        'has_hamburger': has_hamburger,
        'has_layout_js': has_layout_js,
        'len': len(content)
    })

# Find pages that do NOT have hero_banner and do NOT have hero_topbar
missing_header = [r for r in results if not r['has_hero_banner'] and not r['has_hero_topbar']]
print(f"\nPages with NO heroBanner AND NO hero-topbar ({len(missing_header)}):")
for r in missing_header:
    print(f"  {r['path']} (hero_js: {r['has_hero_js']}, layout_js: {r['has_layout_js']}, hamburger: {r['has_hamburger']})")

# Also find pages that have hero_banner or hero_topbar, but missing hamburger
missing_hamburger = [r for r in results if not r['has_hamburger']]
print(f"\nPages with NO hamburger ({len(missing_hamburger)}):")
for r in missing_hamburger:
    print(f"  {r['path']}")

# Also let's inspect pages that have hero_banner but missing hero.js
missing_hero_js = [r for r in results if r['has_hero_banner'] and not r['has_hero_js']]
print(f"\nPages with heroBanner but NO hero.js ({len(missing_hero_js)}):")
for r in missing_hero_js:
    print(f"  {r['path']}")

