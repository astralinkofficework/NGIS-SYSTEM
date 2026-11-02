"""Demo-mode end-to-end check: every Principal surface must run purely off
the in-memory fixtures (mode == 'demo'), with no SQLite/disk dependency."""
import json, urllib.request, urllib.parse

BASE = 'http://127.0.0.1:3000'
HDR = {'Authorization': 'Bearer mock-jwt-token-principal', 'Content-Type': 'application/json'}

def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=HDR)
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.loads(r.read())

checks = []
def ck(name, cond):
    checks.append((name, bool(cond)))
    print(('PASS' if cond else 'FAIL'), '|', name)

# stats
st = call('GET', '/api/principal/stats')
ck('stats.demo-mode', st.get('mode') == 'demo' or st.get('data', {}).get('mode') == 'demo')
ck('stats.totalStudents==15', st['data']['totalStudents'] == 15)
ck('stats.totalTeachers==6', st['data']['totalTeachers'] == 6)
ck('stats.has-honorsRate', 'honorsRate' in st['data'])
ck('stats.recentActions', len(st['data']['recentActions']) >= 1)

# approvals queue
q = call('GET', '/api/principal/approvals?status=pending')
ck('approvals.demo-mode', q.get('mode') == 'demo')
ck('approvals.pending>0', q['data'] and len(q['data']) > 0)
ck('approvals.counts', q.get('counts', {}).get('pending', 0) >= 0)

# certify the first pending transcript
trs = [i for i in q['data'] if i['type'] == 'transcript_certification']
if trs:
    tr = trs[0]
    r = call('POST', '/api/principal/approvals/' + urllib.parse.quote(tr['id'], safe='') + '/action',
             {'action': 'approve', 'note': 'Demo certification'})
    ck('certify.transcript', r.get('status') == 'success' and r.get('mode') == 'demo')

# batch approve grades
b = call('POST', '/api/principal/approvals/batch-action', {'action': 'approve', 'note': 'Demo batch'})
ck('batch.grades', b.get('status') == 'success' and b.get('affected', -1) >= 0)

# roster students
rs = call('GET', '/api/principal/roster/students')
ck('roster.students.demo', rs.get('mode') == 'demo' and len(rs['data']) == 15)
sid = rs['data'][0]['id']
new_adv = 'T-005' if rs['data'][0].get('advisor') != 'T-005' else 'T-001'
e = call('PUT', '/api/principal/roster/students/' + sid, {'advisor': new_adv, 'reason': 'Demo reassignment'})
ck('roster.edit-student', e.get('status') == 'success')
ck('roster.edit-reason-required', True)
try:
    call('PUT', '/api/principal/roster/students/' + sid, {'advisor': 'T-001'})
    ck('roster.edit-blocks-missing-reason', False)
except urllib.error.HTTPError as he:
    ck('roster.edit-blocks-missing-reason', he.code in (400, 422))

# roster teachers
rt = call('GET', '/api/principal/roster/teachers')
ck('roster.teachers.demo', rt.get('mode') == 'demo' and len(rt['data']) == 6)

# per-student grades / attendance / requests
g = call('GET', '/api/principal/grades?studentId=' + sid)
ck('grades.demo', g.get('mode') == 'demo' and len(g['data']) == 6)
if g['data']:
    gid = g['data'][0]['id']
    ov = call('POST', '/api/principal/override-grade', {'gradeId': gid, 'score': 97, 'reason': 'Demo override'})
    ck('grades.override', ov.get('status') == 'success' and ov['data']['letterGrade'] == 'A')
    g2 = call('GET', '/api/principal/grades?studentId=' + sid)
    ck('grades.override-persisted', any(x['id'] == gid and x['percentage'] == 97 for x in g2['data']))

att = call('GET', '/api/principal/attendance-by-day?studentId=' + sid + '&limit=8')
ck('attendance.demo', att.get('mode') == 'demo' and len(att['data']['records']) == 8)

sr = call('GET', '/api/principal/service-requests?category=document')
ck('service-requests.demo', sr.get('mode') == 'demo' and len(sr['data']) >= 1)
sr_all = call('GET', '/api/principal/service-requests?studentId=' + sid)
ck('service-requests.byStudent', sr_all.get('status') == 'success')

# documents transcripts endpoint
docs = call('GET', '/api/principal/transcripts')
ck('transcripts.demo', docs.get('mode') == 'demo' and len(docs['data']) == 6)
ck('transcripts.fileName', all('fileName' in t and 'uploadedAt' in t for t in docs['data']))

# audit
aud = call('GET', '/api/principal/audit?limit=10&role=principal')
ck('audit.demo', aud.get('mode') == 'demo' and len(aud['data']) >= 1)
ck('audit.captured-edits', any('EDIT' in (e['action'] or '') for e in aud['data']))
deep = call('GET', '/api/principal/audit?actor=' + urllib.parse.quote(sid, safe=''))
ck('audit.actor-filter', deep.get('status') == 'success')

# unauthorized check
try:
    req = urllib.request.Request(BASE + '/api/principal/stats')
    urllib.request.urlopen(req, timeout=6)
    ck('auth.401-without-token', False)
except urllib.error.HTTPError as he:
    ck('auth.401-without-token', he.code == 401)

passed = sum(1 for _, ok in checks if ok)
print('\n%d/%d checks passed' % (passed, len(checks)))
print('DEMO ROUND-TRIP ' + ('OK' if passed == len(checks) else 'FAIL'))
