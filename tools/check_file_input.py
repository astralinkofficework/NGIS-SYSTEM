with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<input[^>]*file[^>]*>', text)]
for m in matches:
    print(text[m:m+150])

matches2 = [m.start() for m in re.finditer(r'\.files', text)]
for m in matches2:
    print(text[m-50:m+150])
    print('---')
