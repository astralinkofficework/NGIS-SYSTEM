with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<td[^>]*class=\"[^\"]*action[^\"]*\"[^>]*>[\s\S]*?</td>', text)
print(f"Action TDs in admin-users.html: {len(matches)}")
for m in matches[:3]:
    print(m[:300])

for idx, line in enumerate(text.split('\n')):
    if 'renderUserRow' in line or 'renderTable' in line or 'renderUsers' in line:
        print(f"Line {idx+1}: {line.strip()}")

