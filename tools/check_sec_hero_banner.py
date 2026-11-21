with open('pages/admin/admin-security.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'id=["\']heroBanner["\']', text)]
print("heroBanner occurrences:", len(matches))
for idx in matches:
    print(text[max(0, idx-50):min(len(text), idx+200)])
    print("-" * 30)
