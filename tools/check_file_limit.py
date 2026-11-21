with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'2\s*files|two|fileCount|fileList|uploadedFiles|selectedFiles', text, re.IGNORECASE)]
for m in matches:
    print(text[m-50:m+150])
    print('---')
