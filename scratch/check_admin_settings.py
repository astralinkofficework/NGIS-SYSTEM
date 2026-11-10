with open('pages/admin/admin-settings.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'data-tab=[\'"]([^\'"]+)[\'"]', text)
print('Tabs in admin-settings.html:', matches)
buttons = re.findall(r'<button[^>]+class=[\'"][^\'"]*settings-nav-item[^\'"]*[\'"][^>]*>(.*?)</button>', text, re.DOTALL)
print('Settings nav buttons:', [b.strip() for b in buttons])

