with open('pages/student/student-services.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'// Open / Close New Request Modal[\s\S]*?function selectMobileCategory', text)
if m:
    print('Found old open/close functions:')
    print(m.group(0))
