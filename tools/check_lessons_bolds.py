with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
bolds = re.findall(r'font-(bold|extrabold|black)', text)
print(f"Bold class count: {len(bolds)}")
if bolds:
    print(set(bolds))
