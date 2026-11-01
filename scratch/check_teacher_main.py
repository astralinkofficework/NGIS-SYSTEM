with open('pages/teacher/teacher.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '<div class="main"' in line or 'desktop-view' in line or 'mobile-view' in line or '</div><!-- /.main' in line or '</body>' in line:
        print(f'{i+1}: {line.strip()[:100]}')
