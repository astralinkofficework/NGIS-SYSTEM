with open('pages/principal/principal-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# find renderTable or where rows are mapped
for m in re.finditer(r'<tr.*?</tr>', text, re.DOTALL):
    s = m.group(0)
    if 'action' in s:
        print("Found row with action:")
        print(s[:500])
        print("...")

# Search where tbody.innerHTML is assigned in JS
m = re.findall(r'tbody\.innerHTML\s*=\s*(.*?);', text, re.DOTALL)
for item in m:
    print("\ntbody.innerHTML assignment:")
    print(item[:800])

