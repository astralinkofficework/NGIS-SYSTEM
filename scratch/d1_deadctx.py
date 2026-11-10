import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
def ctx(path, pat, width=160, limit=4):
    t = open(path, encoding='utf-8', errors='replace').read()
    for i, m in enumerate(re.finditer(pat, t)):
        if i >= limit: break
        s = max(0, m.start()-width); e = min(len(t), m.end()+width)
        print(f'  {path}:{t[:m.start()].count(chr(10))+1} ::', ' '.join(t[s:e].split())[:300]); print()
for f, p in [('pages/admin/admin-campus.html', r'admin-(teachers|admins)\.html'),
             ('pages/principal/principal.html', r'campus-announcements\.html'),
             ('pages/student/student-services.html', r'chat\.html'),
             ('pages/teacher/teacher-classes.html', r'class-chats\.html'),
             ('pages/teacher/teacher-roster.html', r'chat\.html')]:
    print('==', f); ctx(f, p)
print('== tests/verify_removal.py ==')
print(open('tests/verify_removal.py', encoding='utf-8', errors='replace').read()[:900])
