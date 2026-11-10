with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Searching commendation:")
for line in text.splitlines():
    if "commendation" in line or "discipline" in line:
        print(line.strip())

