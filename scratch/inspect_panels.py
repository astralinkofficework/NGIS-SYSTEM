with open('assets/css/portal-dashboard.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'([^{}]*(?:ov-inner-panel|ov-feed-panel|ov-feed-list|ov-feed-item)[^{}]*\{[^}]*\})', text)
for m in matches:
    cleaned = m.strip().encode('ascii', errors='replace').decode('ascii')
    print(cleaned[:120].replace('\n', ' '))

