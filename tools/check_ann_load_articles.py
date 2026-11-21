with open('pages/shared/announcements.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'loadArticles|fetch\(url', text):
    s = max(0, m.start()-40)
    e = min(len(text), m.end()+300)
    print(repr(text[s:e]))
