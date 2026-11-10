import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

pages = ['pages/principal/principal-teachers.html',
         'pages/principal/principal-timetables.html',
         'pages/principal/principal-attendance.html']

gone = ['Sync Registry', 'reviewAllBtnText"', '+ Add Timetable Slot',
        'Timetable Management</span>', 'Attendance Ledger &amp; Daily Oversight',
        'Highest school-level authority', 'Master schedule oversight']
for p in pages:
    t = open(p, encoding='utf-8').read()
    hits = [g for g in gone if g in t]
    print(p, '-> leftovers:', hits or 'NONE')

# still-needed references intact?
t1 = open(pages[0], encoding='utf-8').read()
print('openTeacherForm still used (row edit):', t1.count("openTeacherForm("))
t2 = open(pages[1], encoding='utf-8').read()
print('openAddSlotModal still used elsewhere:', t2.count('openAddSlotModal()'))
print('reviewAllBtnText JS guarded:', "if (reviewBtn)" in t1)

# inline script syntax check
for p in pages:
    t = open(p, encoding='utf-8').read()
    scripts = re.findall(r'<script(?![^>]*src)[^>]*>(.*?)</script>', t, re.S)
    bad = 0
    for i, s in enumerate(scripts):
        if not s.strip():
            continue
        f = tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8')
        f.write(s); f.close()
        r = subprocess.run(['node', '--check', f.name], capture_output=True, text=True)
        if r.returncode != 0:
            bad += 1
            print('  SYNTAX ERROR', p, 'script#', i, r.stderr.strip()[:200])
        os.unlink(f.name)
    print(p, 'inline scripts:', len(scripts), 'errors:', bad)
