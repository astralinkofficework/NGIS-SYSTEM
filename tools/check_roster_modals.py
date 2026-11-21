with open('pages/teacher/teacher-roster.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('enrollModal exists:', 'id="enrollModal"' in text)
print('noticeModal exists:', 'id="noticeModal"' in text)
