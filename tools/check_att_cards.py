with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('btnModeCards')
if idx == -1:
    idx = text.find('Cards')
print(repr(text[idx-200:idx+200]))
