with open('test_school_information_e2e.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'persona|switchrole|si-subtitle|subtitle', text, re.IGNORECASE):
    print(text[m.start()-40:m.end()+40])
    print('---')

