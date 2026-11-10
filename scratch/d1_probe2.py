import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def ctx(path, pat, width=90, limit=6):
    t = open(path, encoding='utf-8', errors='replace').read()
    for i, m in enumerate(re.finditer(pat, t)):
        if i >= limit: break
        s = max(0, m.start()-width); e = min(len(t), m.end()+width)
        print(f'  {path}:{t[:m.start()].count(chr(10))+1} ::', ' '.join(t[s:e].split())[:170])

print('--- admin-campus.html refs inside admin-campuses.html ---')
ctx('pages/admin/admin-campuses.html', r'admin-campus\.html')
print('--- server.py backend mentions (prose vs path) ---')
ctx('server.py', r'backend', 60, 8)
print('--- admin-students.html: per-row profile link target ---')
ctx('pages/admin/admin-students.html', r'admin-student-profile\.html', 80, 3)
print('--- admin-users.html: does it link any student profile? ---')
ctx('pages/admin/admin-users.html', r'(profile|student)[\w-]*\.html', 70, 5)
print('--- admin-users.html role filter/param mechanism ---')
ctx('pages/admin/admin-users.html', r'(URLSearchParams|roleParam|searchParams\.get)', 80, 4)
print('--- hero.js admin search block bounds ---')
ctx('assets/js/hero.js', r'ADMIN_SEARCH|adminSearch|type: \x27Student\x27', 70, 3)
