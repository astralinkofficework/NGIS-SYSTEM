with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.rfind('<script>')
print(text[idx:idx+2500])
