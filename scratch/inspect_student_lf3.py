with open('pages/student/student-lost-found.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind('text-right space-x-1.5')
if idx != -1:
    print(text[idx-200:idx+300])

