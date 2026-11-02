with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'href="([^"]*teacher[^"]*)"', text)
print("Teacher links in pages-directory.html:")
for m in sorted(set(matches)):
    print(" -", m)

