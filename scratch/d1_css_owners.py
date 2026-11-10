import re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
names = ['premium-header.js', 'teacher-shared.js', 'bottom-nav.css', 'admin-view.css',
         'portal-dashboard.css', 'announcements.css', 'mvp-redesign.css', 'academic-live.js',
         'teacher-grades.html', 'teacher-grade.html']
files = glob.glob('pages/**/*.html', recursive=True) + glob.glob('pages/**/*.js', recursive=True) \
        + ['index.html', 'sitemap.html', 'pages-directory.html'] + glob.glob('assets/js/*.js') + glob.glob('assets/css/*.css')
for n in names:
    owners = []
    for f in files:
        t = open(f, encoding='utf-8', errors='replace').read()
        c = t.count(n)
        if c and os.path.basename(f) != n:
            owners.append(f'{f}({c})')
    print(f'{n:<22}', owners or 'NO REFS ANYWHERE')
# does gradebook read classId?
g = open('pages/teacher/teacher-gradebook.html', encoding='utf-8', errors='replace').read()
print('gradebook classId usage:', len(re.findall(r'classId', g)))
gr = open('pages/teacher/teacher-grades.html', encoding='utf-8', errors='replace').read()
print('grades classId usage:', len(re.findall(r'classId', gr)))
print('size grades/gradebook:', len(gr), len(g))
u = open('pages/admin/admin-users.html', encoding='utf-8', errors='replace').read()
print('admin-users has student role filter:', bool(re.search(r'(role|filter)[^\n]{0,60}student', u, re.I)), '| URL param handling:', bool(re.search(r'searchParams|location\.search', u)))
