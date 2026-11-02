with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'toggle-sidebar', text)]
print("toggle-sidebar count in teacher.html:", len(matches))
for idx in matches:
    print(text[idx-50:idx+250])
    print("="*40)

