with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("s.status === 'Graded'")
print(repr(text[idx-50:idx+400]))
