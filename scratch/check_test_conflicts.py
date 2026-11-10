with open('scratch/test_timetable_scheduler.py', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'conflicts', text, re.IGNORECASE):
    start = max(0, m.start() - 50)
    end = min(len(text), m.end() + 50)
    print(text[start:end])
    print('---')

