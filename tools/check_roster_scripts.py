with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('tableBody')
if idx == -1:
    idx = text.find('tbody')
print('tbody at:', idx)
print(text[idx-50:idx+250])

import re
matches = [m.start() for m in re.finditer(r'<script', text)]
for m in matches:
    print(text[m:m+120])
