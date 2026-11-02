with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<header[^>]*>([\s\S]*?)</header>', text)
print("Headers in teacher-classes.html:", len(matches))
for m in matches:
    print(m[:400])
    print("="*40)

