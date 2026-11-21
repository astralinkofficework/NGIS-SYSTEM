with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'function serviceWizardNav\([^\)]*\)\s*\{([\s\S]*?)\}', text)
if m:
    print('function serviceWizardNav:')
    print(m.group(0))

m2 = re.search(r'function updateServiceWizardUI\(\)\s*\{([\s\S]*?)\}', text)
if m2:
    print('function updateServiceWizardUI:')
    print(m2.group(0)[:600])
