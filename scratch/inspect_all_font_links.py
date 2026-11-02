import os, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

target_font_link = '<link href="https://fonts.googleapis.com/css2?family=Manrope:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500&family=Inter:wght@300;400;500&family=Kantumruy+Pro:wght@400;500&display=swap" rel="stylesheet">'

for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        c = f.read()
    font_links = re.findall(r'<link[^>]*href=["\']https://fonts\.googleapis\.com/css2\?[^"\']*["\'][^>]*>', c)
    # Check if target is already there or if there are other font links
    safe_print(f'=== {p} ===: {len(font_links)} font links')
    for fl in font_links:
        safe_print('   ' + fl)

