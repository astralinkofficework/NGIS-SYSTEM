with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', text)
for s in scripts:
    if 'fetchItems' in s:
        print("Found fetchItems script block! Length:", len(s))
        lines = s.splitlines()
        for i, line in enumerate(lines[:120]):
            print(f"{i+1}: {line}")
        break

