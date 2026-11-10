import os
import re

for folder in ['pages/admin', 'pages/principal']:
    for f in os.listdir(folder):
        if f.endswith('.html'):
            p = os.path.join(folder, f)
            with open(p, 'r', encoding='utf-8') as fp:
                c = fp.read()
            # check for h1
            h1s = re.findall(r'<h1[^>]*>.*?</h1>(?:\s*<p[^>]*>.*?</p>)?', c, re.DOTALL)
            if h1s:
                for h in h1s:
                    if '<p' in h:
                        print(f'{p}:')
                        print('  ', h.strip()[:150])

