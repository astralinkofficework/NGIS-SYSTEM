import os, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

html_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

matches = []
for p in html_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Find button or a tag with primary colored background classes
    for m in re.finditer(r'<[a-zA-Z0-9\-]+[^>]*class=["\'][^"\']*\b(bg-\[#202F63\]|bg-brand-700|bg-primary-container|bg-ngis|bg-primary\b)[^"\']*["\'][^>]*>', content):
        tag_str = m.group(0)
        if any(b in tag_str for b in ['<button', '<a', 'role="button"', 'type="submit"', 'cursor-pointer']):
            matches.append((p, m.group(1), tag_str[:120]))

safe_print(f'Total primary buttons with blue/brand classes: {len(matches)}')
for p, cls, snippet in matches:
    safe_print(f'[{p}] {cls} -> {snippet}')

