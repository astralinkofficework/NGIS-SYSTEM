import re
s = open('pages/admin/admin-users.html', encoding='utf-8').read()
# find the kebab / more button markup and any adjacent menu
for m in re.finditer(r'<button[^>]*aria-label="More options"[^>]*>.*?</button>', s, re.S):
    print('KEBAB BTN:', re.sub(r'\s+', ' ', m.group(0))[:220])
# any dropdown menu container near it?
print('\nhas action-dropdown:', 'action-dropdown' in s)
print('has data-dropdown-toggle:', 'data-dropdown-toggle' in s)
print('has <div class="menu / dropdown:', bool(re.search(r'class="[^"]*(dropdown|row-menu|kebab-menu|context-menu)[^"]*"', s)))
# handlers referencing more/kebab/menu
for m in re.finditer(r'(onclick|addEventListener)\b[^;]{0,80}(more|kebab|menu|dropdown)[^;]{0,40}', s, re.I):
    print('HANDLER:', re.sub(r'\s+', ' ', m.group(0))[:140])
