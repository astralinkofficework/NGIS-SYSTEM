with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_nm = text.find('id="noticeModal"')
print('noticeModal at:', idx_nm)
print(repr(text[idx_nm-100:idx_nm+300]))

idx_em = text.find('id="enrollModal"')
print('enrollModal at:', idx_em)
print(repr(text[idx_em-100:idx_em+300]))
