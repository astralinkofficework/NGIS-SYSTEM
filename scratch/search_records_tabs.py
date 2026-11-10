with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [line for line in text.splitlines() if 'recordsTeachersTabHtml' in line or 'tab ===' in line or 'recordsTab' in line]
for m in matches:
    print(m)

