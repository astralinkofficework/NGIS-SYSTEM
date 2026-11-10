with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos_admin = text.find('admin: {')
pos_admin_end = text.find('teacher: [')
print('ADMIN GROUPS:')
for m in re.finditer(r'label:\s*\"([^\"]+)\"', text[pos_admin:pos_admin_end]):
    if m.group(1).isupper():
        print(' ', m.group(1))

pos_prl = text.find('principal: {')
pos_prl_end = text.find('const BRAND =')
print('PRINCIPAL GROUPS:')
for m in re.finditer(r'label:\s*\"([^\"]+)\"', text[pos_prl:pos_prl_end]):
    if m.group(1).isupper():
        print(' ', m.group(1))
