with open('pages/principal/principal-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re

m = re.search(r'function renderAttendanceTable\(list\)\s*\{(.*?)\n\}', text, re.DOTALL)
if m:
    print("--- renderAttendanceTable ---")
    print(m.group(0)[:1500])
    print("...")
    print(m.group(0)[-1000:])

