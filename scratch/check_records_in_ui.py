with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'records', text, re.IGNORECASE)]
print('Matches in khmer-suite-ui.js:', len(matches))
for idx in matches[:10]:
    print(text[max(0, idx-50):min(len(text), idx+100)])
    print('---')

