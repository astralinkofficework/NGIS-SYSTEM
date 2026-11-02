import os, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

unique_font_hrefs = set()
for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    hrefs = re.findall(r'href="(https://fonts\.googleapis\.com/css2[^"]*)"', c)
    for h in hrefs:
        unique_font_hrefs.add(h)

safe_print(f'Unique font css2 links across all HTML files: {len(unique_font_hrefs)}')
for h in unique_font_hrefs:
    safe_print('  ' + h)

