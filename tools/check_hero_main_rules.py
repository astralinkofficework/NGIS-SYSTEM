with open('assets/css/hero.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'[^{}]*(?:hero-main|:has\(\.hero-body\))[^{}]*\{[^}]*\}', text)
print(f"Total hero-main rules: {len(matches)}")
for m in matches[:15]:
    print(m.strip()[:200])
    print("---")
