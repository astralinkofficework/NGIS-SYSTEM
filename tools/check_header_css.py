import os, re

search_terms = ['mobile-appbar', 'heroBanner', 'htb-topbar', 'safe-area', 'position: sticky', 'position: fixed']

for file in ['hero.css', 'app.css', 'ui-cleanup.css', 'layout.css']:
    path = os.path.join('assets', 'css', file)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        lines = f.readlines()
        for i, line in enumerate(lines, 1):
            for term in search_terms:
                if term in line:
                    print(f"{file}:{i}: {line.strip()[:100]}")
                    break
