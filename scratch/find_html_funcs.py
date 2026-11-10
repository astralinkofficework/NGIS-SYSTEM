with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

import re
funcs = ['builderHtml', 'viewerHtml', 'subjectsAdminHtml', 'recordsHtml', 'pageHeadHtml', 'kpiHtml']
for fn in funcs:
    matches = [m.start() for m in re.finditer(r'function\s+' + fn, text)]
    print(f"Function {fn}: found at positions {matches}")

