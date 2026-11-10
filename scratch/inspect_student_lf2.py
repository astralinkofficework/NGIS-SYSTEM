with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('openDetailModal', text)]
for idx in matches:
    print(text[idx-50:idx+150])
    print('---')

