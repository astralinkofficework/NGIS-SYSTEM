with open('pages/principal/principal-timetables.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
print('Principal timetables length:', len(c))
endpoints = set(re.findall(r'/api/[a-zA-Z0-9_\-/]+', c))
print('Endpoints in principal-timetables:', endpoints)
scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.DOTALL)
print(f'Found {len(scripts)} scripts')
for i, s in enumerate(scripts):
    print(f'--- Script {i} ({len(s)} chars) ---')
    print(s[:250].strip())

