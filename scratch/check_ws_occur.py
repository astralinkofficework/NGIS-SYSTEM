import sys
with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'workspace-masthead', text)]
print("workspace-masthead occurrences:", len(matches))
for idx in matches:
    print(text[idx-50:idx+150])
    print('---')

