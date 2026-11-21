with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// Window Public Methods')
print(text[idx:idx+400])
