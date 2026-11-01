with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
scripts = re.findall(r'<script\s+src=[\'"]([^\'"]+)[\'"]', text)
for s in scripts:
    print(s)
