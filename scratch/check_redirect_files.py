for f in ['admin-principals.html', 'admin-teachers.html', 'teacher-grade.html']:
    p = f'pages/admin/{f}' if 'admin' in f else f'pages/teacher/{f}'
    try:
        with open(p, 'r', encoding='utf-8') as file:
            print(f, file.read()[:200].replace('\n', ' '))
    except Exception as e:
        print(f, 'Error:', e)

