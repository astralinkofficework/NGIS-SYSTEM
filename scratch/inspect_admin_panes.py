with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Searching tab panes in admin.html:")
for m in re.finditer(r'id=[\"\']pane[A-Za-z0-9]+[\"\']', text):
    print(m.group(0))

