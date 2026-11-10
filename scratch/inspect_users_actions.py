with open('pages/admin/admin-users.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'<td[^>]*class="[^"]*(?:table-actions|text-right)[^"]*"[^>]*>.*?</td>', text, re.DOTALL)
for m in matches:
    print("admin-users td:", m.strip()[:300])

# Also search for table row template in JS
m2 = re.findall(r'<tr.*?</tr>', text, re.DOTALL)
for r in m2:
    if 'action' in r:
        print("tr with action:")
        print(r[:400])

