with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('Sheet Grid')
print(repr(text[idx-300:idx]))
