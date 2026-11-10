with open('pages/principal/principal-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

# Find tbody
tbody_m = re.search(r'<tbody[^>]*id=["\']([^"\']*)["\'][^>]*>(.*?)</tbody>', text, re.DOTALL)
if tbody_m:
    print(f"tbody ID: {tbody_m.group(1)}")
    print(f"tbody static length: {len(tbody_m.group(2))}")
    rows = re.findall(r'<tr[^>]*>', tbody_m.group(2))
    print(f"Static <tr> count in tbody: {len(rows)}")

# Find JS functions relating to table rendering or data
print("\nJS matches for table render/load:")
for m in re.finditer(r'function\s+(?:render|load|filter|update|populate)[A-Za-z0-9_]*', text):
    print(m.group(0))

for m in re.finditer(r'arrival-oversight-table|tbody', text):
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 100)
    print("--- Ref ---")
    print(text[start:end])

