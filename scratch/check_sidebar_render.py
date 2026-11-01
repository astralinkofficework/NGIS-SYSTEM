with open('assets/js/layout.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'(renderSidebar|buildSidebar|sidebar-link|data-id|addEventListener\([\'"]click)', text)]
print('Matches in layout.js:', len(matches))
for m in matches[:15]:
    snippet = text[max(0, m-40):min(len(text), m+120)].replace('\n', ' ')
    print(snippet.encode('ascii', errors='replace').decode('ascii'))
    print('---')

