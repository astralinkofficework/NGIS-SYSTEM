with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<header[^>]*>([\s\S]*?)</header>', text)
print("Headers in student-lost-found:", len(matches))
for m in matches:
    print(m[:300])
    print("="*40)

# Check toggle-sidebar
toggles = re.findall(r'toggle-sidebar', text)
print("toggle-sidebar count:", len(toggles))

