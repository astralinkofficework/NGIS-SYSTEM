import os

for path in ['pages/admin/admin-school-information.html', 'pages/principal/principal-school-information.html', 'assets/js/school-information.js']:
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            c = f.read()
        print(f'=== {path} ===')
        for term in ['h1', 'si-subtitle', 'Persona:', 'switchRole', 'Manage institutional']:
            print(f'  {term} count: {c.count(term)}')

