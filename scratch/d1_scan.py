import re, os, sys, glob
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

candidates = {
 'unused_assets': ['shared-components.css','teacher-portal.css','app.js','error-boundary.js','premium-header.js','teacher-shared.js'],
 'teacher_dead': ['teacher-grade.html','teacher-grades.html'],
 'admin_shadow': ['admin-accounts.html','admin-admins.html','admin-attendance.html','admin-audit.html',
                  'admin-campus.html','admin-principals.html','admin-student-profile.html','admin-students.html','admin-teachers.html'],
 'shared_offline': ['exams.html','lessons.html','news.html','onboarding.html'],
 'legacy_servers': ['server-v2.js','server-complete.js','server-enhanced.js','backend'],
}

# live surfaces = pages/**, *.html at root, assets/**, academic_store.py, server.py, tests/**
live_files = (glob.glob('pages/**/*.html', recursive=True) + glob.glob('pages/**/*.js', recursive=True)
              + ['index.html','sitemap.html','pages-directory.html']
              + glob.glob('assets/**/*.js', recursive=True) + glob.glob('assets/**/*.css', recursive=True)
              + glob.glob('assets/components/*.js')
              + glob.glob('tests/**/*', recursive=True)
              + ['server.py','academic_store.py','layout.js'])
live_files = [f for f in live_files if os.path.isfile(f)]

cache = {f: open(f, encoding='utf-8', errors='replace').read() for f in live_files}

def find_refs(name, exclude_self=True):
    hits = []
    for f, txt in cache.items():
        if exclude_self and os.path.basename(f) == name:
            continue
        n = txt.count(name)
        if n:
            hits.append((f, n))
    return hits

for group, names in candidates.items():
    print(f'== {group} ==')
    for name in names:
        hits = find_refs(name)
        # also substring 'backend/' in server.py
        print(f'  {name}: ' + ('NO LIVE REFS' if not hits else str(hits[:8]) + (' +' + str(len(hits)-8) + ' more' if len(hits) > 8 else '')))

# what does server.py say about backend/ and the js servers?
svr = cache['server.py']
for m in re.finditer(r'.{70}backend.{70}', svr):
    print('server.py backend ctx:', m.group(0).replace('\n', ' ')[:150])
print('server.py static route style:', re.findall(r"send_from_directory\([^)]*\)", svr)[:4] or re.findall(r"STATIC|PAGES_DIR", svr)[:4])
