import sys
with open('pages/teacher/teacher-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
matches = re.findall(r'(\.(?:ws-select-btn|ws-cmd-btn|ws-icon-btn|workspace-masthead)[^\{]*\{[^\}]*\})', text)
for m in matches:
    sys.stdout.buffer.write(m.encode('utf-8'))
    sys.stdout.buffer.write(b'\n---\n')

