with open('pages/teacher/teacher-reports.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('publishSingle')
if idx != -1:
    print(text[idx-50:idx+600])

