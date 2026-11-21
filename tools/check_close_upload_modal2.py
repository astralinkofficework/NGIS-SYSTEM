with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('closeUploadModal')
while idx != -1:
    print('Found at', idx)
    print(repr(text[idx-50:idx+150]))
    idx = text.find('closeUploadModal', idx+1)
