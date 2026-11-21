with open('server.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'/api/exams', text)]
for m in matches:
    start = max(0, m - 50)
    end = min(len(text), m + 200)
    print("--- MATCH ---")
    print(text[start:end])
