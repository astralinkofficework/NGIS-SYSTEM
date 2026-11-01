with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer('js/hero.js', text)]
print('Matches for js/hero.js:', matches)
for m in matches:
    print(text[m-30:m+50].replace('\n', ' '))

