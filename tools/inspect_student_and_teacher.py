with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("student.html mains:")
for m in re.finditer(r'<main[^>]*>', text):
    print(" ", m.group(0))

with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    t_text = f.read()

print("\nteacher-attendance.html mains:")
for m in re.finditer(r'<main[^>]*>', t_text):
    print(" ", m.group(0))
