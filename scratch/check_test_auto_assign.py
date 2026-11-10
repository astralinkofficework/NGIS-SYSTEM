with open('scratch/test_timetable_scheduler.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'btnAutoGenerate|auto-assign', text):
    print(text[m.start()-50:m.end()+50])

