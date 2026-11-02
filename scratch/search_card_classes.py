import os
import re

html_files = []
for root, dirs, fnames in os.walk('.'):
    if any(p in root for p in ['.git', 'node_modules', '.agents', '.system_generated', 'scratch']):
        continue
    for f in fnames:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

results = []
for path in html_files:
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check for card elements with hover effects
    # Find tags containing card, ws-card, hub-card, etc.
    cards = re.findall(r'<[a-zA-Z0-9\-]+[^>]*class="[^"]*(?:card|ws-card|stat|panel|module|hub|dept)[^"]*"[^>]*>', content)
    for c in cards:
        if any(h in c for h in ['hover:bg-', 'hover:border-', 'hover:shadow-', 'group-hover:']):
            results.append((path, c[:140]))

print(f'Total card tags with hover: {len(results)}')
for p, c in results:
    print(f'[{p}] {c}')

