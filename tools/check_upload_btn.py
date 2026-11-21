with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = [m.start() for m in re.finditer(r'openUploadTranscriptModal', text)]
for m in matches:
    print(text[m-80:m+150])
    print('---')
