with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<input[^>]*search[^>]*>', text, re.IGNORECASE)]
for m in matches:
    print(text[m:m+200])
