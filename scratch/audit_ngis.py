import re, glob, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

lay = open('assets/js/layout.js', encoding='utf-8').read()
m = re.search(r'.{120}[Ss]taff.{120}', lay)
print('staff context:', repr(m.group(0)) if m else 'none')

svr = open('server.py', encoding='utf-8', errors='replace').read()
print('routes:', len(re.findall(r'@app.route', svr)))
print('DEMO flags:', re.findall(r'^[A-Z_]*DEMO[A-Z_]*\s*=\s*.+', svr, re.M)[:6])
print('ACADEMIC. calls:', svr.count('ACADEMIC.'), '| DB[ calls:', len(re.findall(r'DB\[', svr)))

# nav entries per role in layout.js
for role in ('student', 'teacher', 'principal', 'admin'):
    seg = re.search(r"%s:\s*\[(.*?)\]\s*[,}]" % role, lay, re.S)
    if seg:
        ids = re.findall(r'id:\s*"([^"]+)"', seg.group(1))
        print(f'{role} nav ({len(ids)}):', ids)
    else:
        print(f'{role}: nav block not found by regex')

# teacher grade-family pages: what are they?
for f in ['teacher-grade.html', 'teacher-grades.html', 'teacher-gradebook.html', 'teacher-roster.html', 'teacher-submissions.html']:
    p = 'pages/teacher/' + f
    try:
        h = open(p, encoding='utf-8', errors='replace').read()
        t = re.search(r'<title>(.*?)</title>', h, re.S)
        c = re.search(r'window\.PAGE\s*=\s*(\{[^)]*\})', h)
        print(f, '|', (t.group(1).strip() if t else '?'), '|', (c.group(1).strip()[:70] if c else '?'))
    except FileNotFoundError:
        print(f, 'MISSING')
