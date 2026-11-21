with open('pages/teacher/teacher-lessons.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('lesson-details')
if idx != -1:
    print('Found lesson-details at', idx)
    print(text[idx-50:idx+250])
else:
    print('lesson-details not found in teacher-lessons.html!')
