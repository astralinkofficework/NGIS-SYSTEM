import os, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

files = []
for root, dirs, fnames in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in fnames:
        if f.endswith(('.css', '.html')):
            files.append(os.path.join(root, f))

button_rules = []
for p in files:
    if p.endswith('.css'):
        with open(p, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        for m in re.finditer(r'([^{}]+)\{([^{}]+)\}', content):
            sel, body = m.group(1).strip(), m.group(2).strip()
            if any(k in sel for k in ['btn-primary', 'ngis-btn-primary', 'ov-btn-main', 'primary-btn', 'btn_primary']):
                button_rules.append((p, sel, body))

safe_print(f'Button rules found in CSS: {len(button_rules)}')
for p, s, b in button_rules:
    safe_print(f'[{p}] {s}\n    {b[:100]}...\n')

