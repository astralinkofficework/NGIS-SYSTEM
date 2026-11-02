import os

css_files = [
    'assets/css/app.css',
    'assets/css/hero.css',
    'assets/css/teacher-portal.css',
    'pages/student/css/base.css',
    'pages/student/css/hero.css'
]

for p in css_files:
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            c = f.read()
        c = c.replace(", Roboto", "").replace(", 'Roboto'", "").replace(', "Roboto"', '')
        with open(p, 'w', encoding='utf-8') as f:
            f.write(c)

print('Cleaned font fallbacks!')

