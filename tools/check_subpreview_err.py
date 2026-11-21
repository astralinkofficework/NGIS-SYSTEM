with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('subPreviewZoom')
print(text[idx-200:idx+300])
