for p in ['pages/admin/admin-exams.html', 'pages/admin/admin-lessons.html']:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"=== {p} ===")
    idx = text.find('<tbody>')
    if idx != -1:
        print(text[idx:idx+1200])

