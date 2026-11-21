import os
import re

for root, dirs, files in os.walk('assets/js'):
    for f in files:
        if f.endswith('.js'):
            p = os.path.join(root, f)
            with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                c = fp.read()
            if 'modal' in c.lower() or 'dialog' in c.lower() or 'drawer' in c.lower():
                matches = re.findall(r'id=["\']([^"\']*(?:modal|dialog|drawer)[^"\']*)["\']', c, re.I)
                if matches:
                    print(f"{f:30}: {sorted(list(set(matches)))[:6]}")
