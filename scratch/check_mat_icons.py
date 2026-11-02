import os, re

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

has_mat_icon_in_font = []
for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    links = re.findall(r'<link[^>]*href=["\'][^"\']*fonts\.googleapis\.com[^"\']*["\'][^>]*>', c)
    for l in links:
        if 'Material+Symbols' in l:
            has_mat_icon_in_font.append((p, l))

print(f'Pages with Material Symbols in Google Font link: {len(has_mat_icon_in_font)}')
for p, l in has_mat_icon_in_font[:10]:
    print(f'{p}: {l}')

