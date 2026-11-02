with open('assets/css/design-system.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'([^{}]*card[^{}]*\{[^}]*\})', text, re.I)
print(f"Cards in design-system.css: {len(matches)}")
for m in matches[:10]:
    print(' '.join(m.split())[:120])

