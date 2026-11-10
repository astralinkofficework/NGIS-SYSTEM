import re, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
files = ['pages/admin/admin-classes.html','pages/admin/admin-department-detail.html','pages/admin/admin-departments.html',
         'pages/admin/admin-lifecycle.html','pages/admin/admin-timetables.html','pages/admin/admin-users.html',
         'pages/principal/principal-profile.html','pages/principal/principal-reports.html',
         'pages/shared/departments.html','pages/student/student-lost-found.html','pages/student/student-services.html',
         'pages/teacher/teacher-classes.html','pages/teacher/teacher-lessons.html']
for f in files:
    t = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(r'(?:chat|shared/chat|messaging/[\w-]+)\.html', t):
        s = max(0, m.start()-120); e = min(len(t), m.end()+60)
        line = t[:m.start()].count('\n')+1
        print(f'{f}:{line} :: ' + ' '.join(t[s:e].split())[:210])
        print()
