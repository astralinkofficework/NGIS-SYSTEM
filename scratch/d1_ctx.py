import re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def ctx(path, pat, width=110):
    try:
        t = open(path, encoding='utf-8', errors='replace').read()
    except FileNotFoundError:
        print(path, 'MISSING'); return
    for m in re.finditer(pat, t):
        s = max(0, m.start()-width); e = min(len(t), m.end()+width)
        print(f'  {path}:{t[:m.start()].count(chr(10))+1} ::', ' '.join(t[s:e].split())[:200])

print('--- app.js refs in layout.js / app.css ---')
ctx('assets/js/layout.js', r'app\.js')
ctx('assets/css/app.css', r'app\.js')
print('--- error-boundary refs in layout.js ---')
ctx('assets/js/layout.js', r'error-boundary')
print('--- shared-components ref in design-system.css ---')
ctx('assets/css/design-system.css', r'shared-components')
print('--- teacher-grades.html refs in teacher-departments.html ---')
ctx('pages/teacher/teacher-departments.html', r'teacher-grades\.html')
print('--- hero.js refs to admin shadow pages ---')
ctx('assets/js/hero.js', r'admin-(admins|principals|students|teachers)\.html', 60)
print('--- admin.html refs to shadow pages ---')
ctx('pages/admin/admin.html', r'admin-(attendance|students)\.html')
print('--- admin-lifecycle refs ---')
ctx('pages/admin/admin-lifecycle.html', r'admin-(attendance|students)\.html')
print('--- admin-grades refs ---')
ctx('pages/admin/admin-grades.html', r'admin-(audit|student-profile)\.html')
print('--- admin-department-detail refs ---')
ctx('pages/admin/admin-department-detail.html', r'admin-teachers\.html')
print('--- tests refs ---')
for f in ['tests/e2e-portals.test.py','tests/test_gradebook_viewport.py','tests/test_all_portals_ui_clean.py','tests/test_ui_states_mvp.py','tests/apply_user_removal.py','tests/test_all_portals_viewport.py']:
    ctx(f, r'(teacher-grades|admin-(attendance|students))\.html', 60)
