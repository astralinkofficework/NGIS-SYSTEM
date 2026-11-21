with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'onclick=[\"\'][^\"\']*(?:student-assignments|student-timetable|student-grades|lessons)[^\"\']*[\"\']', text)
for m in matches:
    print(m)
