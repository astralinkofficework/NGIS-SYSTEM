with open("assets/js/khmer-suite-ui.js", "r", encoding="utf-8") as f:
    text = f.read()

import re
matches = [l for l in text.splitlines() if any(k in l for k in ['formatKhmerSubjectName', 'shiftNameKh', 'classMasterModernHtml', 'renderMasterRow', 'teacherMasterModernHtml'])]
print(f"Matches count: {len(matches)}")
for m in matches[:15]:
    print(" ", m.strip()[:100])

