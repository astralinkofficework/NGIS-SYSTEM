with open('tests/test_khmer_suite.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'records', text, re.IGNORECASE)]
print('Matches in test_khmer_suite.py:', len(matches))
for idx in matches:
    print(text[max(0, idx-50):min(len(text), idx+100)])
    print('---')

