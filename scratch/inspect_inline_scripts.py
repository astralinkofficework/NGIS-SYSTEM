with open('pages/admin/admin-timetables.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.DOTALL)
print(f'Found {len(scripts)} inline script blocks')
for i, s in enumerate(scripts):
    print(f'--- Script {i} ({len(s)} chars) ---')
    print(s[:300].strip())
    print('...')

