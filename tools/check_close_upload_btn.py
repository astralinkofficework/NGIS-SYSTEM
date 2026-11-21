with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('closeUploadBtn')
while idx != -1:
    print('Found at', idx)
    print(text[idx-50:idx+200])
    idx = text.find('closeUploadBtn', idx+1)
