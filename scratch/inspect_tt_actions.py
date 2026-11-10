import re

with open('pages/principal/principal-timetables.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<td[^>]*table-actions[^>]*>.*?</td>', text, re.DOTALL):
    print("timetables td:")
    print(m.group(0))

