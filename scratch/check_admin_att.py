with open('pages/admin/admin-attendance.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()[:40]
print(''.join(lines))
