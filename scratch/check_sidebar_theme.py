with open('assets/css/app.css', 'r', encoding='utf-8') as f:
    c = f.read()

import re
matches = [m.group(0) for m in re.finditer(r'\[data-theme="[^"]*"\]\s*\.sidebar[^{]*\{', c)]
print('Theme matches for sidebar:', matches)

