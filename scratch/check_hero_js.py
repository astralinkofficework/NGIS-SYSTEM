with open('pages/teacher/js/hero.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'toggle-sidebar', text)]
print("toggle-sidebar in hero.js:", len(matches))
for idx in matches:
    print(text[idx-50:idx+250])

