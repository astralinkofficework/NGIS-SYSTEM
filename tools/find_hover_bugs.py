import os
import re

admin_dir = 'pages/admin'
for fname in sorted(os.listdir(admin_dir)):
    if not fname.endswith('.html'):
        continue
    fpath = os.path.join(admin_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Check for buttons or links with hover:text-white without dark bg
    elements = re.findall(r'<([a-zA-Z0-9]+)[^>]*class=["\']([^"\']+)["\'][^>]*>', text)
    bad = []
    for tag, cls in elements:
        classes = cls.split()
        if 'hover:text-white' in classes or 'hover:text-slate-50' in classes or 'hover:text-gray-50' in classes:
            # check if dark:hover or if there is a dark hover:bg
            has_dark_prefix = any(c.startswith('dark:hover:text-white') for c in classes)
            has_dark_bg_hover = any(c.startswith('hover:bg-') and any(d in c for d in ['slate-800', 'slate-900', 'gray-800', 'gray-900', 'emerald-800', 'emerald-700', 'brand-800', 'brand-900', 'brand-700', 'zinc-800', 'zinc-900', 'black']) for c in classes)
            has_static_dark_bg = any(c.startswith('bg-') and any(d in c for d in ['slate-800', 'slate-900', 'gray-800', 'gray-900', 'emerald-800', 'emerald-700', 'brand-800', 'brand-900', 'brand-700', 'zinc-800', 'zinc-900', 'black']) for c in classes)
            
            if not has_dark_prefix and not has_dark_bg_hover and not has_static_dark_bg:
                bad.append((tag, cls))
    if bad:
        print(f"=== {fname} ({len(bad)} dangerous elements) ===")
        for tag, cls in bad[:5]:
            print(f"  <{tag} class='{cls[:120]}'>")
