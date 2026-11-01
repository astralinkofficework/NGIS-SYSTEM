for f in ['exams.html', 'lessons.html', 'news.html', 'access-denied.html']:
    p = f'pages/shared/{f}'
    with open(p, 'r', encoding='utf-8', errors='ignore') as file:
        text = file.read()
        import re
        matches = re.findall(r'(?:window\.)?location\.(?:href|replace)\s*=\s*[\'"`]([^\'"`]+)[\'"`]|window\.PAGE\s*=\s*({[^}]+})', text)
        print(f'{f}:', matches)

