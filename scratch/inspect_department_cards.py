with open(r'pages\shared\department.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = text.find('Lessons & Materials')
if pos != -1:
    print(text[max(0, pos-400):min(len(text), pos+1500)])

