with open(r'C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7\VISUAL_TIMETABLE_SCHEDULER_REPORT.md', 'r', encoding='utf-8') as f:
    text = f.read()

import re
for m in re.finditer(r'toolbar', text, re.IGNORECASE):
    print(text[m.start()-30:m.end()+100])
    print('---')

