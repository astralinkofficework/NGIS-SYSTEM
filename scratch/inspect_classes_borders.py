with open('pages/principal/principal-classes.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
print('Classes page card borders:')
for m in re.finditer(r'class="[^"]*(?:card|border|rounded)[^"]*"', c[:4000]):
    print(' ', m.group(0))

