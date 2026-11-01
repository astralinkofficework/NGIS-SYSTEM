with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div class="main"' in line or '</div><!-- /.student-desktop-view -->' in line or 'studentMobileView' in line or '</div><!-- /.main' in line or '</body>' in line:
        print(f'{i+1}: {line.strip()[:100]}')
