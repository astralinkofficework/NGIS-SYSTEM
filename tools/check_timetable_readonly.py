with open('pages/student/student-timetable.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print('Has edit/add in timetable:', 'edit' in text.lower() or 'add' in text.lower())
# Search for buttons in timetable
buttons = re.findall(r'<button[^>]*>(.*?)</button>', text, re.IGNORECASE)
print(f'Total buttons in timetable HTML: {len(buttons)}')
for b in buttons:
    print('  Button:', b.strip()[:60])
