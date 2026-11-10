with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// Action button')
if idx != -1:
    print(text[idx:idx+800])

