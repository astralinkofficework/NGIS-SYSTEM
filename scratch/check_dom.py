with open('pages/student/student.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    for key in ['class="shell"', 'id="calPopupOverlay"', 'student-mobile-view', 'student-desktop-view', 'id="htbDropdown"', 'id="htbNotifPanel"']:
        if key in line:
            print(f'Line {i+1}: {line.strip()[:100]}')
