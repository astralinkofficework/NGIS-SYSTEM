with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'NGIS_PAGES', text)]
for idx in matches:
    print(text[idx-20:idx+250])
    print("="*40)

