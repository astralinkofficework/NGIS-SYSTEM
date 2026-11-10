with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.finditer(r'admin-news|school-information|admin-school', text)
for m in matches:
    idx = m.start()
    print("Match at index", idx)
    print(text[max(0, idx-150):min(len(text), idx+200)])
    print("-" * 50)
