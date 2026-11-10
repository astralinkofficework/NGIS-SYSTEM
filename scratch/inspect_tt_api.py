with open('timetable_api.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
routes = re.findall(r'@timetable_bp\.route\([^\)]*\)\s+def\s+[a-zA-Z0-9_]+', text)
print('timetable_api.py routes:')
for r in routes:
    print(' ', r.replace('\n', ' '))

