with open('pages/principal/principal-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'id=["\']correctionModal["\'].*?</div>\s*</div>\s*</div>', text, re.DOTALL)
if m:
    print("--- Correction Modal ---")
    print(m.group(0)[:600])

m2 = re.search(r'id=["\']snapshotModal["\'].*?</div>\s*</div>\s*</div>', text, re.DOTALL)
if m2:
    print("--- Snapshot Modal ---")
    print(m2.group(0)[:600])

