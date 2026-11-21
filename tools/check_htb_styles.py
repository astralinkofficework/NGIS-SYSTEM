with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'[^{}]*\.htb-[^{}]*\{[^}]*\}', text)
print(f"Total .htb- rules: {len(matches)}")
for m in matches:
    if 'color' in m or 'background' in m or 'border' in m:
        if 'htb-ctrl-btn' in m or 'htb-search' in m or 'htb-chip' in m:
            print(m.strip()[:200])
            print("---")
