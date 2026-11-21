import glob
import re

css_files = glob.glob('assets/css/*.css')

patterns = [
    r'card.*:hover',
    r'card.*:active',
    r':hover.*background',
    r'hub-card',
    r'dept-card',
    r'portal-card',
    r'background:\s*transparent',
    r'background-color:\s*transparent',
    r'pointerdown'
]

print('Searching CSS files...')
for file in css_files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if 'hover' in line.lower() and ('card' in line.lower() or 'hub' in line.lower() or 'dept' in line.lower()):
            if 'background' in line or 'transform' in line or 'opacity' in line or 'border' in line or '{' in line:
                print(f'{file}:{i+1}: {line.strip()[:90]}')
