with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<main[^>]*>', text)
print("Main tags in teacher-classes.html:", matches)

