import re

with open('pages/principal/principal-classes.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<td[^>]*table-actions[^>]*>.*?</td>', text, re.DOTALL):
    print("classes table-actions td:", m.group(0))
