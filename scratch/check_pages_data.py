with open('all_pages_data.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\{[^\{\}]*role:\s*[\'"]teacher[\'"][^\{\}]*\})', text)
print("Teacher pages count in all_pages_data.js:", len(matches))
for m in matches[:3]:
    print(m)
    print("---")

