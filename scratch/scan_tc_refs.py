import re, sys, glob, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
name = 'teacher-classes.html'
live = glob.glob('pages/**/*.html', recursive=True) + glob.glob('assets/js/*.js') + glob.glob('assets/components/*.js') \
       + ['index.html', 'sitemap.html', 'pages-directory.html', 'all_pages_data.js', 'all_pages_data.json', 'layout.js'] \
       + glob.glob('tests/**/*.py')
for f in live:
    if os.path.basename(f) == name: continue
    t = open(f, encoding='utf-8', errors='replace').read()
    for m in re.finditer(re.escape(name), t):
        s = max(0, m.start()-80); e = min(len(t), m.end()+50)
        print(f'{f}:{t[:m.start()].count(chr(10))+1} ::', ' '.join(t[s:e].split())[:160])
# does teacher-roster accept classId? (candidate rewire target)
r = open('pages/teacher/teacher-roster.html', encoding='utf-8', errors='replace').read()
print('--- teacher-roster classId support:', len(re.findall(r'classId', r)))
d = open('pages/teacher/teacher.html', encoding='utf-8', errors='replace').read()
print('--- teacher.html classId support:', len(re.findall(r'classId', d)))
