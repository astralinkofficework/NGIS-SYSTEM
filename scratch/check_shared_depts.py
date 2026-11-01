with open('pages/shared/departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'(location\.href|teacher|student|role|protect|_auth|redirect)', text, re.IGNORECASE)]
print('Matches in shared/departments.html:', len(matches))
for m in matches[:15]:
    snippet = text[max(0, m-40):min(len(text), m+80)].replace('\n', ' ')
    print(snippet.encode('ascii', errors='replace').decode('ascii'))

