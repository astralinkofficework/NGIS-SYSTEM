with open('exam_management_api.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'/api/exams', text)]
print(f"Found {len(matches)} matches in exam_management_api.py")
for m in matches[:5]:
    start = max(0, m - 40)
    end = min(len(text), m + 150)
    print("--- MATCH ---")
    print(text[start:end])
