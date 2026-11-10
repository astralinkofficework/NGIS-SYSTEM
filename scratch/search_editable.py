with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'TEACHER_EDITABLE_FIELDS' in line]
for m in matches:
    print(m)

