import os, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

primary_button_elements = []
for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Match <button> or <a> with primary indicators
    buttons = re.findall(r'<[a-zA-Z0-9\-]+[^>]*class=["\'][^"\']*(?:btn-primary|ngis-btn-primary|ov-btn-main|bg-\[#202F63\]|bg-primary|bg-brand-700|bg-ngis|bg-primary-container)[^"\']*["\'][^>]*>[\s\S]*?</[a-zA-Z0-9\-]+>', content)
    for b in buttons:
        # ignore nav-link or non-button elements if any
        if any(tag in b[:20] for tag in ['<button', '<a', '<input']):
            # get tag opening
            tag_open = re.match(r'<[^>]+>', b).group(0)
            text_snippet = re.sub(r'<[^>]+>', '', b).strip()[:40]
            primary_button_elements.append((p, tag_open, text_snippet))

safe_print(f'Total primary buttons found: {len(primary_button_elements)}')
for p, tag, txt in primary_button_elements[:30]:
    safe_print(f'[{p}] "{txt}" -> {tag[:100]}')

