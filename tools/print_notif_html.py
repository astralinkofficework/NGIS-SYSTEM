with open('pages/student/student-notifications.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
m = re.search(r'<main[\s\S]*?</main>', text)
if m:
    print(m.group(0)[:3000])
