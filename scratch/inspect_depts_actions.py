import re

with open('pages/principal/principal-departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'<td[^>]*text-right[^>]*>.*?</td>', text, re.DOTALL):
    print("text-right td:", m.group(0))

# Also search for "View Syllabi"
idx = text.find('View Syllabi')
if idx != -1:
    print("\nFound View Syllabi:")
    print(text[idx-200:idx+400])
