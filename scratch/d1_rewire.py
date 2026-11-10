# D1 rewire migration: repoint every live reference away from pages we are about to delete.
import re, sys, json
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

REWIRES = [
    # (file, old substring, new substring)
    ('pages/teacher/teacher-departments.html', 'teacher-grades.html', 'teacher-gradebook.html'),
    ('pages/admin/admin.html', 'admin-students.html', 'admin-users.html?role=students'),
    ('pages/admin/admin-lifecycle.html', 'admin-students.html', 'admin-users.html?role=students'),
    ('pages/admin/admin-campus.html', 'admin-students.html', 'admin-users.html?role=students'),
    ('pages/admin/admin-grades.html', 'admin-audit.html', 'admin-logs.html'),
    ('pages/admin/admin-grades.html', "'admin-student-profile.html'", "'admin-settings.html'"),
    ('pages/admin/admin-department-detail.html', 'admin-teachers.html', 'admin-users.html?role=teachers'),
    ('assets/js/hero.js', "href: 'admin-students.html'", "href: 'admin-users.html?role=students'"),
    ('assets/js/hero.js', "href: 'admin-teachers.html'", "href: 'admin-users.html?role=teachers'"),
    ('assets/js/hero.js', "href: 'admin-admins.html'", "href: 'admin-users.html?role=admins'"),
    ('assets/js/hero.js', "href: 'admin-principals.html'", "href: 'admin-users.html?role=principals'"),
    ('tests/e2e-portals.test.py', 'pages/teacher/teacher-grades.html', 'pages/teacher/teacher-gradebook.html'),
    ('tests/test_gradebook_viewport.py', 'pages/teacher/teacher-grades.html', 'pages/teacher/teacher-gradebook.html'),
    ('tests/test_all_portals_ui_clean.py', 'pages/admin/admin-students.html', 'pages/admin/admin-users.html'),
    ('tests/test_ui_states_mvp.py', 'pages/admin/admin-students.html', 'pages/admin/admin-users.html?role=students'),
]

changed = {}
for path, old, new in REWIRES:
    t = open(path, encoding='utf-8').read()
    n = t.count(old)
    if n == 0:
        print(f'  MISS  {path}: "{old}" not found')
        continue
    t2 = t.replace(old, new)
    open(path, 'w', encoding='utf-8').write(t2)
    changed[path] = changed.get(path, 0) + n
    print(f'  OK    {path}: {old} -> {new} ({n}x)')
print('files touched:', len(changed))

# directory feeds: report entries for pages we will delete
GONE = ['admin-accounts.html','admin-admins.html','admin-audit.html','admin-principals.html',
        'admin-students.html','admin-student-profile.html','admin-teachers.html',
        'teacher-grade.html','teacher-grades.html']
for feed in ('all_pages_data.json',):
    data = json.load(open(feed, encoding='utf-8'))
    hits = json.dumps(data)
    print(feed, 'mentions of doomed pages:', {g: hits.count(g) for g in GONE if g in hits} or 'none')
for feed in ('all_pages_data.js', 'sitemap.html', 'pages-directory.html', 'index.html'):
    t = open(feed, encoding='utf-8', errors='replace').read()
    hits = {g: t.count(g) for g in GONE if g in t}
    print(feed, '->', hits or 'none')
