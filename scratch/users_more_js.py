import re
s = open('pages/admin/admin-users.html', encoding='utf-8').read()
# how is btn-more / data-action="more" handled?
print('=== btn-more / more handling ===')
for m in re.finditer(r'.{60}btn-more.{140}', s):
    print(' ', re.sub(r'\s+', ' ', m.group(0))[:200])
print('\n=== closeAllDropdowns / dropdown builders ===')
for m in re.finditer(r'(function\s+\w*[Dd]ropdown\w*|closeAllDropdowns|openRowMenu|buildMenu|showMenu)\b', s):
    ln = s[:m.start()].count('\n') + 1
    print('  line', ln, m.group(0))
print('\n=== candidate row action functions (reset/suspend/profile/toggle) ===')
for kw in ['resetPassword', 'reset_password', 'suspend', 'toggleActive', 'viewProfile', 'openProfile', 'deactivate', 'changeStatus']:
    hits = [s[:m.start()].count('\n') + 1 for m in re.finditer(kw, s)]
    if hits:
        print('  %-14s lines=%s' % (kw, hits[:6]))
print('\n=== any <div class="...menu..."> markup ===')
for m in re.finditer(r'<div[^>]*class="[^"]*(?:menu|dropdown|popover)[^"]*"[^>]*>', s):
    print('  ', re.sub(r'\s+', ' ', m.group(0))[:140])
