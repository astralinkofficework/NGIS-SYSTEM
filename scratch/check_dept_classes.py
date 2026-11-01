with open('pages/shared/department.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<div class="[^"]*stat[^"]*"|<section[^>]*>|<div class="hub-[^"]*"', text)
print(matches[:20])

