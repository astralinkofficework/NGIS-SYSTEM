import glob
import re

html_files = glob.glob('**/*.html', recursive=True)
hardcoded_sidebars = []
layout_js_sidebars = []

for h in html_files:
    if '.kilo' in h or 'node_modules' in h:
        continue
    with open(h, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    has_sidebar_html = ('<aside' in content) or ('class="sidebar' in content) or ('id="sidebar"' in content)
    has_layout_js = ('layout.js' in content)
    has_nav_items = ('nav-link' in content or 'nav-item' in content or 'side-nav' in content)
    
    if has_sidebar_html and has_nav_items:
        hardcoded_sidebars.append(h)
    elif has_layout_js:
        layout_js_sidebars.append(h)

print(f"Total HTML files: {len(html_files)}")
print(f"HTML files with hardcoded sidebar markup: {len(hardcoded_sidebars)}")
for f in hardcoded_sidebars:
    print("  HARDCODED:", f)

print(f"\nHTML files using layout.js: {len(layout_js_sidebars)}")

