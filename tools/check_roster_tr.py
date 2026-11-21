with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<tr', text)]
print('Total <tr in roster:', len(matches))
for m in matches[3:8]:
    print(repr(text[m:m+120]))
    print('---')
