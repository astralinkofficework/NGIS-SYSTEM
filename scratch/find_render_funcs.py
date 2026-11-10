with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = re.findall(r'render[A-Z][a-zA-Z0-9_]*', text)
print('Render functions in school-information.js:')
for fn in set(funcs):
    print(' -', fn)

