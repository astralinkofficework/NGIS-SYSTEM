with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('window.closeUploadModal')
print(text[idx:idx+600])
