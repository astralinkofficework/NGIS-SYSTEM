with open('pages/student/student-notifications.html', 'r', encoding='utf-8') as f:
    text = f.read()

print("Length of student-notifications.html:", len(text))
import re
print("API calls / storage keys in student-notifications.html:")
for m in re.finditer(r'(?:fetch\([^\)]*\)|localStorage\.[a-zA-Z0-9_]+|[A-Z_]+_KEY|notif[a-zA-Z0-9_]*)', text):
    print(m.group(0))
