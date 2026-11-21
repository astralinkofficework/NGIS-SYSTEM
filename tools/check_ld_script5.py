with open('pages/shared/lesson-details.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', text)
print(scripts[4])
