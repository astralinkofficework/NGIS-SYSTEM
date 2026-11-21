with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

import re
print("Hamburger matches in teacher.html:")
for m in re.finditer(r'<button[^>]*hamburger[^>]*>', text, re.I):
    print(m.group(0))

for m in re.finditer(r'<button[^>]*toggle-sidebar[^>]*>', text, re.I):
    print(m.group(0))

idx_head = text.find('id="mobile')
if idx_head != -1:
    print(text[idx_head-50:idx_head+500])
else:
    idx_main = text.find('<main')
    print(text[idx_main:idx_main+800])
