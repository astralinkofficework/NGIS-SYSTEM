import glob
import re

for cf in ['assets/css/app.css', 'assets/css/portal-dashboard.css', 'assets/css/shared-components.css', 'assets/css/hero.css']:
    with open(cf, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    print(f"=== {cf} ===")
    matches = re.findall(r'([^{}]*\bmain\b[^{}]*\{[^}]*\})', text)
    for m in matches[:5]:
        print(m.strip().replace('\n', ' ')[:120])

