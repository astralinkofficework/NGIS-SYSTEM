with open('pages/principal/principal-timetables.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'function toggleScheduleRow\s*\(.*?\)\s*\{.*?\n\}', text, re.DOTALL)
if m:
    print(m.group(0))

