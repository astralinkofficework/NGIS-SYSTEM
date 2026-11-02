import os, re, sys

def safe_print(t):
    sys.stdout.buffer.write((str(t) + '\n').encode('utf-8', errors='replace'))

css_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.css'):
            css_files.append(os.path.join(root, f))

fonts_found = []
for p in css_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        if 'font-family' in l or '--font' in l or '--token-font' in l:
            fonts_found.append((p, i+1, l.strip()))

safe_print(f'Font declarations found: {len(fonts_found)}')
for p, lnum, l in fonts_found[:40]:
    safe_print(f'{p}:{lnum} -> {l}')

