with open(r'pages\shared\department.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
pos = text.find('Report Cards')
print(text[max(0, pos-300):min(len(text), pos+1500)])

