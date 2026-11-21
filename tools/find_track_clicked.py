with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'.{0,60}Track clicked links.{0,60}', text)
if m:
    print(repr(m.group(0)))
