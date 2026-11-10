with open('pages/principal/principal-teacher-profiles.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Found in principal-teacher-profiles.html:")
for m in re.finditer(r'<div[^>]*telemetry-card[^>]*>', text):
    start = m.start()
    print(text[start:start+300])

