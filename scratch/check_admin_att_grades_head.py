for p in ['pages/admin/admin-attendance.html', 'pages/admin/admin-grades.html']:
    with open(p, 'r', encoding='utf-8') as f:
        text = f.read()
    print(f"action-icons in {p}:", 'action-icons' in text)

