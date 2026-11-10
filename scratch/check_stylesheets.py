import re

pages = [
    'pages/principal/principal.html',
    'pages/admin/admin.html',
    'pages/teacher/teacher.html',
    'pages/student/student.html',
    'index.html'
]

for p in pages:
    print(f"=== {p} ===")
    with open(p, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()
    for m in re.finditer(r'<link[^>]*rel=["\']stylesheet["\'][^>]*>', text):
        print(" ", m.group(0))

