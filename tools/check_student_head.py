with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
head = text[:text.find('</head>')]
print(head)
