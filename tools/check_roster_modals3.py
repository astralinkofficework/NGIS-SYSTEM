with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx_nm = text.find('id="noticeModal"')
idx_em = text.find('id="enrollModal"')
# What comes after enrollModal?
idx_after_em = text.find('</form>', idx_em)
idx_after_em2 = text.find('</div>\n\n  </div>', idx_after_em)
print('End of enrollModal around:', idx_after_em2)
print(repr(text[idx_after_em2:idx_after_em2+200]))
