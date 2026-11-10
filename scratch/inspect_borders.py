with open('assets/js/khmer-suite-ui.js', 'r', encoding='utf-8') as f:
    text = f.read()

start = text.find('function wizardHtml()')
end = text.find('function attachWizardInteractions()')
wcode = text[start:end]

import re
print('Borders in wizardHtml:')
for m in re.finditer(r'border(?:-[a-z0-9/]+)?', wcode):
    print(m.group(0))

