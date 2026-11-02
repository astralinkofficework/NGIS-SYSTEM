with open('all_pages_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\{[^\{\}]*student-lost-found\.html[^\{\}]*\})', text)
for m in matches:
    print(m)

