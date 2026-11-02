import json, urllib.request, urllib.error

BASE = 'http://localhost:3000'

def call(path, token=None, method='GET', body=None):
    req = urllib.request.Request(BASE + path, method=method)
    if token:
        req.add_header('Authorization', 'Bearer ' + token)
    data = None
    if body is not None:
        data = json.dumps(body).encode()
        req.add_header('Content-Type', 'application/json')
    try:
        with urllib.request.urlopen(req, data, timeout=10) as r:
            return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except Exception:
            return e.code, {}

P = 'mock-jwt-token-principal'
S = 'mock-jwt-token-student'
T = 'mock-jwt-token-teacher'
results = []

code, j = call('/api/principal/approvals')
results.append(('approvals no-auth -> 401', code == 401))
code, j = call('/api/principal/approvals', S)
results.append(('approvals student -> 403', code == 403))
code, j = call('/api/principal/approvals', P)
items = j.get('data', [])
results.append(('approvals principal 200 w/ items', code == 200 and len(items) > 0))
print('queue:', [(i['id'], i['status']) for i in items][:12])
print('counts:', j.get('counts'))

code, j = call('/api/principal/stats', P)
d = j.get('data', {})
results.append(('stats real', code == 200 and d.get('totalStudents', 0) > 0 and d.get('totalStudents') != 1250))
print('stats:', {k: v for k, v in d.items() if k != 'recentActions'})

code, j = call('/api/principal/roster/students', P)
rows = j.get('data', [])
results.append(('roster students', code == 200 and len(rows) > 0 and 'gpaLive' in rows[0]))
code, j = call('/api/principal/roster/teachers', P)
trows = j.get('data', [])
results.append(('roster teachers', code == 200 and len(trows) > 0 and 'pendingGradeRecords' in trows[0]))

# Edit a student record (with reason) and verify persistence + audit
sid = rows[0]['id']
old_adv = rows[0].get('advisor')
code, j = call(f'/api/principal/roster/students/{sid}', P, 'PUT', {'reason': 'Test correction', 'advisor': 'Mr. Chea Sophea'})
results.append(('student edit needs reason -> ok', code == 200 and j.get('status') == 'success'))
code, j = call(f'/api/principal/roster/students/{sid}', P, 'PUT', {'advisor': 'Dr. Sarah Jenkins'})
results.append(('student edit without reason -> 400', code == 400))
# revert
code, j = call(f'/api/principal/roster/students/{sid}', P, 'PUT', {'reason': 'Revert test edit', 'advisor': old_adv})
results.append(('student edit revert', code == 200))

# Approval workflow: find a pending grade group, return it, then approve it
gg = next((i for i in items if i['type'] == 'grade_submission'), None)
if gg:
    key = gg['id']
    code, j = call(f'/api/principal/approvals/{key}/action', P, 'POST', {'action': 'needs_correction', 'note': 'Please re-check Q4 rubric'})
    results.append(('return grade group', code == 200))
    code, j = call('/api/principal/approvals?status=needs_correction', P)
    back = [i for i in j.get('data', []) if i['id'] == key]
    results.append(('group visible as needs_correction', len(back) == 1))
    code, j = call(f'/api/principal/approvals/{key}/action', P, 'POST', {'action': 'approve', 'note': ''})
    results.append(('approve after revision', code == 200))
    code, j = call('/api/principal/approvals?status=pending', P)
    gone = [i for i in j.get('data', []) if i['id'] == key]
    results.append(('group no longer pending', len(gone) == 0))
    # verify the workflow actually flipped in sqlite via oversight
    code, j = call('/api/academic/admin/oversight', P)
    print('oversight:', j.get('data', {}).get('pendingGrades'), 'pending /', j.get('data', {}).get('publishedGrades'), 'published')

# request decision round-trip
rq = next((i for i in items if i['type'] == 'service_request'), None)
if rq:
    code, j = call(f"/api/principal/approvals/{rq['id']}/action", P, 'POST', {'action': 'approve', 'note': 'Certificate issued'})
    results.append(('request approve', code == 200))
    code, j = call(f"/api/service-requests/{rq['requestId']}", P)
    st = j.get('data', {}).get('status')
    results.append(('service request synced to completed', st == 'completed'))
    print('request', rq['requestId'], 'status now:', st)

# audit
code, j = call('/api/principal/audit?limit=5', P)
results.append(('audit real events', code == 200 and len(j.get('data', [])) > 0))
print('audit top:', [e['action'] for e in j.get('data', [])][:5])

print('\n=== RESULTS ===')
fails = 0
for name, ok in results:
    print(('PASS' if ok else 'FAIL'), '-', name)
    fails += 0 if ok else 1
print('FAILED:', fails)
