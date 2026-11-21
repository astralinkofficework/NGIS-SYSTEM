with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('btnViewCardsDesk')
print(repr(text[idx-400:idx]))
