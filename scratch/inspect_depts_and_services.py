with open('pages/principal/principal-departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

m = re.search(r'function renderTable\s*\(.*?\)\s*\{.*?\n\}', text, re.DOTALL)
if m:
    print("=== principal-departments.html renderTable ===")
    print(m.group(0)[:2500])

with open('pages/principal/principal-services.html', 'r', encoding='utf-8') as f:
    stext = f.read()

# Search for render or table body in services
m2 = re.search(r'function render[^{]*\{.*?\n\}', stext, re.DOTALL)
if m2:
    print("\n=== principal-services.html render ===")
    print(m2.group(0)[:2500])
else:
    # search where serviceRequests or tbody is modified
    tbody_idx = stext.find('tbody')
    print("tbody found at:", tbody_idx)
    # search for innerHTML =
    for m in re.finditer(r'\.innerHTML\s*=\s*`', stext):
        print("innerHTML template at:", m.start())
        print(stext[m.start():m.start()+800])

