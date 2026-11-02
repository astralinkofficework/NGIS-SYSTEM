import os, re, sys

print("Scanning for card hover/touch/click interactions...")

card_patterns = [
    r'(\.[a-zA-Z0-9_\-]*card[a-zA-Z0-9_\-]*:hover[^{]*\{[^}]*\})',
    r'(\.[a-zA-Z0-9_\-]*card[a-zA-Z0-9_\-]*:active[^{]*\{[^}]*\})',
    r'(\.[a-zA-Z0-9_\-]*card[a-zA-Z0-9_\-]*::before[^{]*\{[^}]*\})',
    r'(\.[a-zA-Z0-9_\-]*card[a-zA-Z0-9_\-]*::after[^{]*\{[^}]*\})',
]

for root, dirs, files in os.walk('.'):
    if any(ign in root for ign in ['.git', 'node_modules', '.system_generated', 'skills']):
        continue
    for f in files:
        if f.endswith(('.css', '.html', '.js')):
            path = os.path.join(root, f)
            try:
                with open(path, 'r', encoding='utf-8') as fp:
                    content = fp.read()
                    
                    # Check JS ripple / circle creation
                    if f.endswith('.js') or '<script' in content:
                        for term in ['ripple', 'createRipple', 'radial', 'pointerdown', 'mouseenter', 'mousemove', 'overlay', 'highlight']:
                            if term in content:
                                for line_idx, line in enumerate(content.splitlines()):
                                    if any(k in line.lower() for k in ['ripple', 'circle', 'createripple', 'radial-gradient']) and any(c in line.lower() for c in ['card', 'item', 'button', 'target', 'elem', 'this', 'click', 'event', 'touch']):
                                        print(f"JS hit: {path}:{line_idx+1}: {line.strip()[:100]}")
                                        
                    # Check CSS
                    if f.endswith('.css') or '<style' in content:
                        for term in ['ripple', 'radial-gradient', 'border-radius: 50%', 'border-radius: 9999px', 'border-radius: 100%']:
                            if term in content:
                                for line_idx, line in enumerate(content.splitlines()):
                                    if any(k in line.lower() for k in ['radial-gradient', 'ripple']):
                                        print(f"CSS hit: {path}:{line_idx+1}: {line.strip()[:100]}")
            except Exception as e:
                pass

