for p in [
    'assets/css/app.css',
    'pages/admin/admin-lifecycle.html',
    'pages/teacher/teacher-lessons.html',
    'pages/shared/departments.html'
]:
    with open(p, 'r', encoding='utf-8') as f:
        c = f.read()
    c = c.replace('Cinzel', 'Manrope')
    c = c.replace('cinzel', 'manrope')
    c = c.replace('Roboto', 'Manrope')
    c = c.replace('roboto', 'manrope')
    with open(p, 'w', encoding='utf-8') as f:
        f.write(c)

print('Cleaned remaining 4 files!')

