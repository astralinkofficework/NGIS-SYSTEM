with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("s.status === 'Graded'")
idx2 = text.find("s.status === 'Graded'", idx + 1)
print(repr(text[idx2-50:idx2+750]))
