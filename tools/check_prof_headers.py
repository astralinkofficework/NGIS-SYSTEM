files = [
    'pages/admin/admin-teacher-profiles.html',
    'pages/admin/admin-student-profiles.html',
    'pages/principal/principal-teacher-profiles.html',
    'pages/principal/principal-student-profiles.html'
]
for f in files:
    with open(f, encoding='utf-8') as fp:
        lines = fp.readlines()
        for i, line in enumerate(lines, 1):
            if '<header class="lg:hidden' in line:
                print(f"{f}:{i}:")
                for j in range(i-1, min(i+15, len(lines))):
                    print("  " + lines[j].strip())
