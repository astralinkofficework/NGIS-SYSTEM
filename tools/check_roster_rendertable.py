with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('function renderTable(')
print(text[idx:idx+1500])
