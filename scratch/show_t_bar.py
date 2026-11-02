with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('data-action="toggle-sidebar"')
print(text[idx-400:idx+400])

