with open('assets/js/exams-simple.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'data-action', text):
    start = max(0, m.start() - 30)
    end = min(len(text), m.end() + 60)
    print(repr(text[start:end]))
