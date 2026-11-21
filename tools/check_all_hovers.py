import os
import re

css_dir = 'assets/css'
for fname in sorted(os.listdir(css_dir)):
    if not fname.endswith('.css'):
        continue
    fpath = os.path.join(css_dir, fname)
    with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    
    # Clean comments
    clean = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    # Find rules
    blocks = re.findall(r'([^{}]+)\{([^{}]+)\}', clean)
    for sel, body in blocks:
        if ':hover' in sel and ('btn' in sel or 'button' in sel or 'action' in sel or '[role="button"]' in sel or 'a:' in sel):
            # check body for color or background
            lines = [l.strip() for l in body.split(';') if l.strip()]
            color_prop = [l for l in lines if l.startswith('color')]
            bg_prop = [l for l in lines if 'background' in l]
            if color_prop or bg_prop:
                print(f"[{fname}] {sel.strip()[:60]} => color: {color_prop}, bg: {bg_prop}")
