with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'toggle-sidebar', text)]
print("toggle-sidebar in teacher-attendance:", len(matches))
for idx in matches:
    print(text[idx-50:idx+250])

