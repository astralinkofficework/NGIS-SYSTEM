with open('pages/teacher/teacher-submissions.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('subPreviewZoom')
idx2 = text.find('subPreviewZoom', idx+1)
idx3 = text.find('subPreviewZoom', idx2+1)
print(text[idx3-200:idx3+200])
