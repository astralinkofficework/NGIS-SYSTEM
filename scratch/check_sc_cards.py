import sys
with open('assets/css/shared-components.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'([^{}]*card[^{}]*\{[^}]*\})', text, re.I)
print(f"Cards in shared-components.css: {len(matches)}")
for m in matches[:15]:
    sys.stdout.buffer.write((' '.join(m.split())[:120] + '\n').encode('utf-8'))

