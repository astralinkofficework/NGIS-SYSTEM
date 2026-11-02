with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(teacher-[a-zA-Z0-9_\-\.]+)', text)
print("Teacher pages in pages-directory.html:", set(matches))

