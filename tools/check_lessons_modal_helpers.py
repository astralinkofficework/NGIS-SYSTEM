with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('// Modal helpers')
idx_end = text.find('window.exportLessonsCSV', idx)
print(text[idx:idx_end])
