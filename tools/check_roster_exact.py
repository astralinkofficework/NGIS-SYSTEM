with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_nm = text.find('id="noticeModal"')
idx_prev_comment = text.rfind('<!--', 0, idx_nm)
print('idx_prev_comment at:', idx_prev_comment)
print(repr(text[idx_prev_comment:idx_nm+50]))

idx_main = text.find('</main>', idx_nm)
print('idx_main at:', idx_main)
