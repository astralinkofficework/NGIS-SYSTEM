import os

with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'data-act="conflicts"' in l or 'data-act=\'conflicts\'' in l or 'conflicts' in l.lower() and 'button' in l.lower():
        print(f'{i+1}: {l.strip()[:120]}')

