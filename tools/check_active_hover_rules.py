import glob
import re

css_files = glob.glob('assets/css/*.css')

print('--- CHECKING :active rules ---')
for file in css_files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    matches = re.findall(r'([^}\n]*:active[^\{]*)\{([^}]+)\}', content)
    for sel, body in matches:
        if 'card' in sel or 'hub' in sel or 'dept' in sel or 'background' in body:
            print(f'{file} -> {sel.strip()[:60]} : {body.strip()[:60]}')

print('\n--- CHECKING :hover with background: transparent or background: none ---')
for file in css_files:
    with open(file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    matches = re.findall(r'([^}\n]*:hover[^\{]*)\{([^}]+)\}', content)
    for sel, body in matches:
        if ('background: transparent' in body or 'background: none' in body or 'background-color: transparent' in body):
            if 'nav' not in sel and 'btn-ghost' not in sel and 'close' not in sel:
                print(f'{file} -> {sel.strip()[:70]} : {body.strip()[:60]}')
