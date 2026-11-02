import os, re

approved_fonts = [
    'manrope',
    'plus jakarta sans',
    'inter',
    'kantumruy pro',
    'material symbols outlined',
    'material icons',
    'phosphor',
    'phosphor-bold',
    'phosphor-fill',
    'system-ui',
    '-apple-system',
    'blinkmacsystemfont',
    'segoe ui',
    'sans-serif',
    'serif',
    'monospace',
    'inherit',
    'var('
]

css_files = []
for root, dirs, files in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']): continue
    for f in files:
        if f.endswith('.css'):
            css_files.append(os.path.join(root, f))

non_approved_declarations = []
for p in css_files:
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for i, l in enumerate(lines):
        if 'font-family:' in l:
            # check if any non-approved font is in there
            for bad in ['cinzel', 'playfair', 'outfit', 'lexend', 'poppins', 'roboto']:
                if bad in l.lower():
                    non_approved_declarations.append((p, i+1, l.strip()))

print(f'Non-approved font declarations in CSS: {len(non_approved_declarations)}')
for p, lnum, l in non_approved_declarations:
    print(f'{p}:{lnum} -> {l}')

