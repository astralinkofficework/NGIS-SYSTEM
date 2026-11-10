import re
s = open('pages/admin/admin-users.html', encoding='utf-8').read()
# grab the dropdown-menu-list template (row kebab menu items)
m = re.search(r'dropdown-menu-list.{0,900}', s, re.S)
if m:
    print('MENU TEMPLATE:\n', re.sub(r'\s+', ' ', m.group(0))[:900])
print('\n=== icon mechanism inside menu items ===')
for mm in re.finditer(r'dropdown-menu-item[^>]*>(.{0,120})', s, re.S):
    frag = re.sub(r'\s+', ' ', mm.group(1))[:120]
    if 'material-symbols' in frag or 'data-ngis-icon' in frag or '<svg' in frag:
        print('  ', frag)
        break
print('\nmenu item icon types present:')
print('  material in menu region:', s.count('dropdown-menu-item'))
