import os, glob, re

pages = glob.glob('pages/**/*.html', recursive=True)

no_toggle_pages = []
for p in sorted(pages):
    norm_p = p.replace('\\', '/')
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    has_toggle = 'data-action="toggle-sidebar"' in content or 'data-toggle="sidebar"' in content
    if not has_toggle:
        # Check what is at top of <main class="main">
        m = re.search(r'<main[^>]*>(.*?)(?:<div|<section|<table)', content, re.DOTALL | re.I)
        snippet = m.group(1).strip() if m else ''
        
        # Check if heroBanner is there
        has_hb = 'id="heroBanner"' in content
        
        no_toggle_pages.append((norm_p, has_hb, snippet[:100].replace('\n', ' ')))

print(f"Total pages without toggle-sidebar ({len(no_toggle_pages)}):")
for p, hb, snip in no_toggle_pages:
    print(f"  {p} | has_heroBanner={hb} | top_snippet: {snip}")

