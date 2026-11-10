with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'\.page\b[^{]*\{[^}]*\}', text)
for m in matches[:5]:
    print(m)
    print('---')

