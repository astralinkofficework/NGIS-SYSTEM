with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'[^\n]*(?:topbar|heroBanner|mobileMainAppbar)[^\n]*', text)
print(f"Total occurrences in layout.js: {len(matches)}")
for m in matches[:20]:
    print(m.strip()[:100])
