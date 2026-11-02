"""End-to-end verification for the Principal Central Management System."""
import json
import urllib.error
import urllib.request

BASE = 'http://127.0.0.1:3000'
PRN = {'Authorization': 'Bearer mock-jwt-token-principal'}
STU = {'Authorization': 'Bearer mock-jwt-token-student'}

def get(path, headers=PRN):
    req = urllib.request.Request(BASE + path, headers=headers)
    with urllib.request.urlopen(req, timeout=6) as r:
        return r.status, r.read()

def status_only(path, headers=PRN):
    try:
        req = urllib.request.Request(BASE + path, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code

fails = []
def check(label, cond, extra=''):
    print(('OK  ' if cond else 'FAIL') + ' :: ' + label + ((' :: ' + extra) if extra else ''))
    if not cond: fails.append(label)

# 1. Principal page HTML loads (200) and contains the expected PAGE active marker
# (name, marker, strict) — strict pages require hamburger + auth bootstrap
PAGES = [
    ('principal.html',                              '"active":"dashboard"', True),
    ('principal-approvals.html',                    'NGISAuth.api',            True),
    ('principal-students.html',                     '"active":"students"',  True),
    ('principal-teachers.html',                     '"active":"teachers"',  True),
    ('principal-documents.html',                    '"active":"documents"', True),
    ('principal-activity.html',                     '"active":"activity"',  True),
    ('principal-reports.html',                      None,                   False),
    ('principal-profile.html',                      None,                   False),
]
for name, marker, strict in PAGES:
    try:
        code, body = get('/pages/principal/' + name)
        text = body.decode('utf-8', 'ignore')
        ok = code == 200 and ('principal' in text.lower())
        if marker: ok = ok and (marker in text)
        if strict:
            ok = ok and ('data-action="toggle-sidebar"' in text or 'toggle-sidebar' in text)
            ok = ok and ('_auth-bootstrap.js' in text)
        check('GET /pages/principal/' + name, ok)
    except Exception as e:
        check('GET /pages/principal/' + name, False, str(e))

# 2. Principal APIs (all should require auth -> 200 with header, 401 without)
APIS = [
    '/api/principal/stats',
    '/api/principal/approvals',
    '/api/principal/roster/students',
    '/api/principal/roster/teachers',
    '/api/principal/audit?limit=5',
    '/api/academic/transcripts',
    '/api/service-requests?category=document',
]
for path in APIS:
    try:
        code, body = get(path)
        payload = json.loads(body)
        check('API 200 ' + path, code == 200 and ('data' in payload or 'status' in payload or 'items' in payload))
    except Exception as e:
        check('API 200 ' + path, False, str(e))
    # enforce: without bearer -> 401 (except transcripts/service-requests which are public read)
    if path.startswith('/api/principal/'):
        unauthorized = status_only(path, headers={})
        check('API 401 unauth ' + path, unauthorized == 401, str(unauthorized))

# 3. Stats shape (real numbers, no demo defaults)
code, body = get('/api/principal/stats')
stats = json.loads(body)['data']
check('stats.totalStudents real', isinstance(stats.get('totalStudents'), int) and stats['totalStudents'] > 0, str(stats.get('totalStudents')))
check('stats.totalTeachers real', isinstance(stats.get('totalTeachers'), int) and stats['totalTeachers'] > 0, str(stats.get('totalTeachers')))
check('stats.pendingApprovals present', 'pendingApprovals' in stats)
check('stats.recentActions array', isinstance(stats.get('recentActions'), list))
check('stats has no fake 1480/86', stats.get('totalStudents') != 1480 and stats.get('totalTeachers') != 86)

# 4. Audit endpoint accepts actor filter (used by teachers page deep-link)
code, body = get('/api/principal/audit?actor=does-not-exist')
payload = json.loads(body)
check('audit actor filter returns list', isinstance(payload.get('data'), list))

# 5. Roster endpoints
rs = json.loads(get('/api/principal/roster/students')[1])
check('roster students has classes list', isinstance(rs.get('classes'), list) and len(rs['classes']) > 0)
sample = rs['data'][0]
check('roster student has live gpa field', 'gpaLive' in sample and 'openRequests' in sample, str(list(sample.keys())[:8]))
rt = json.loads(get('/api/principal/roster/teachers')[1])
check('roster teachers has pending count', len(rt['data']) > 0 and 'pendingGradeRecords' in rt['data'][0])

# 6. Approvals queue derived, not demo
ap = json.loads(get('/api/principal/approvals')[1])
items = ap['data']
check('approvals queue has counts', 'counts' in ap)
check('approvals items have type + id', all('type' in i and 'id' in i for i in items))
prefixes = {i['id'].split(':')[0] for i in items}
check('approvals derived (grade/request/transcript prefixes)', prefixes.issubset({'grade', 'request', 'transcript'}), str(prefixes))

# 7. Old demo constant should be gone
import re, io
src = io.open('server.py', encoding='utf-8').read()
check('PRINCIPAL_APPROVALS demo list removed', 'PRINCIPAL_APPROVALS = [' not in src)
check('server has new persistence layer', 'SERVICE_REQUESTS_FILE' in src and 'STUDENTS_OVERLAY_FILE' in src)
check('audit actor param added', "request.args.get('actor')" in src)

# 8. Sidebar wiring (both layout.js copies)
assets = io.open('assets/js/layout.js', encoding='utf-8').read()
root = io.open('layout.js', encoding='utf-8').read()
check('layout.js copies identical', assets == root)
for token in ('principal-students.html', 'principal-teachers.html', 'principal-documents.html', 'principal-activity.html'):
    check('sidebar references ' + token, token in assets)

# 9. No student-sidebar pollution (existing student nav entry kept)
check('student nav untouched', 'pages/student/student.html' in assets)

print()
if fails:
    print('FAILURES:', len(fails)); [print(' -', f) for f in fails]; raise SystemExit(1)
print('ALL PRINCIPAL SYSTEM CHECKS PASSED')
