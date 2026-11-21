with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('selectStudent', text)]
for m in matches:
    print(text[m-50:m+100])
    print('---')
