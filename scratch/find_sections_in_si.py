with open('assets/js/school-information.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<h[23][^>]*>.*?</h[23]>(?:\s*<p[^>]*>.*?</p>)?', text)
for m in matches[:10]:
    print(m[:120])
    print('---')

