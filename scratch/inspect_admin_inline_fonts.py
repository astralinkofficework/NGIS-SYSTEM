import re

with open('pages/admin/admin.html', 'r', encoding='utf-8') as f:
    text = f.read()

for m in re.finditer(r'style=["\'][^"\']*font-family:[^"\']*["\']', text):
    print(m.group(0)[:100])

