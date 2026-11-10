with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<td[^>]*>[\s\S]*?(?:button|onclick|action)[\s\S]*?</td>', text)
print(f"Action TDs in teacher-roster.html: {len(matches)}")
for m in matches[:5]:
    print(m[:200])

for idx, line in enumerate(text.split('\n')):
    if 'render' in line.lower() and 'function' in line.lower():
        print(f"Line {idx+1}: {line.strip()}")

