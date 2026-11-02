with open('pages-directory.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script.*?>([\s\S]*?)</script>', text)
for s in scripts:
    if 'pages' in s.lower() and len(s) > 100:
        print("Found script, length:", len(s))
        for line in s.splitlines()[:50]:
            print(line)
        break

