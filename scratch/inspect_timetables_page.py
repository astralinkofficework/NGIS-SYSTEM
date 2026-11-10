with open('pages/admin/admin-timetables.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
print('Script tags:')
for s in re.findall(r'<script[^>]*src=[\'"][^\'"]+[\'"][^>]*>', c):
    print(' ', s)

print('API endpoints mentioned:')
endpoints = set(re.findall(r'/api/[a-zA-Z0-9_\-/]+', c))
for ep in sorted(endpoints):
    print(' ', ep)

