with open('pages/shared/announcements.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'(location\.href|location\.replace|window\.PAGE|role)', text)]
print('Matches in shared/announcements.html:', len(matches))
for m in matches[:10]:
    print(text[max(0, m-30):min(len(text), m+70)].replace('\n', ' ').encode('ascii', errors='replace').decode('ascii'))

