with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'<table', text)]
for idx in matches:
    print(text[idx:idx+600])
    print('---')

