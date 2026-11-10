with open('pages/admin/admin-timetables.html', 'r', encoding='utf-8') as f:
    c = f.read()

import re
scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', c, re.DOTALL)
print(scripts[4])

