with open('pages/teacher/teacher-attendance.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('id="btnViewGridDesk"')
print(text[idx-250:idx])
