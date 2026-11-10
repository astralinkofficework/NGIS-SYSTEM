with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderTable')
if idx != -1:
    print(text[idx:idx+1500])

