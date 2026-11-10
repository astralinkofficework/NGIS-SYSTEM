with open('assets/css/khmer-suite.css', 'r', encoding='utf-8') as f:
    text = f.read()

import re
classes = ['ks-workflow-bar', 'ks-sheet-tabs', 'ks-page-head', 'ks-kpi-strip', 'ks-wf-step']
for c in classes:
    matches = [m.start() for m in re.finditer(r'\.' + c, text)]
    print(f"Class .{c}: {len(matches)} matches")
    if matches:
        pos = matches[0]
        print(text[pos:pos+300])
        print("---")

