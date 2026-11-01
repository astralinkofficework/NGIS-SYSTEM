with open('pages/teacher/teacher-departments.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('8 Faculty Members')
print(repr(text[idx-50:idx+200]))

