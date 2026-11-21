with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [l.strip()[:100] for l in text.splitlines() if 'createElement("script")' in l or "createElement('script')" in l]
for m in matches:
    print(m)
