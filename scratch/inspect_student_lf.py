with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<td[^>]*table-actions[^>]*>.*?</td>', text, re.DOTALL)
for m in matches:
    print("student-lost-found td:", m.strip())
