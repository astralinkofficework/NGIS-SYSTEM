with open('pages/teacher/teacher-gradebook.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<td[^>]*actions[^>]*>(.*?)</td>', text, re.IGNORECASE | re.DOTALL)
print(f"Found {len(matches)} action td matches in teacher-gradebook.html")
for m in matches[:5]:
    print("---")
    print(m.strip()[:200])
