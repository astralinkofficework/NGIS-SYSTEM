with open('pages/shared/lesson-details.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script[^>]*>([\s\S]*?)</script>', text)
for i, s in enumerate(scripts):
    if len(s.strip()) > 0:
        print(f"--- Script {i+1} ---")
        print(s[:500])
