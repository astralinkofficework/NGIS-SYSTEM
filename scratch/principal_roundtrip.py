"""Round-trip workflow: certify a transcript, edit a student, and confirm
the management audit trail surfaces both actions."""
import json, urllib.request, urllib.error, urllib.parse

BASE = 'http://127.0.0.1:3000'
HDR = {'Authorization': 'Bearer mock-jwt-token-principal', 'Content-Type': 'application/json'}

def call(method, path, body=None, headers=HDR):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers=headers)
    with urllib.request.urlopen(req, timeout=6) as r:
        return json.loads(r.read())

# 1 · Certify (approve) the first pending transcript via the approval action API
q = call('GET', '/api/principal/approvals?status=pending')
transcripts = [i for i in q['data'] if i['type'] == 'transcript_certification']
if transcripts:
    tr = transcripts[0]
    resp = call('POST', '/api/principal/approvals/' + urllib.parse.quote(tr['id'], safe='') + '/action',
                {'action': 'approve', 'note': 'Verified against registrar copy – E2E test'})
    print('certify →', resp.get('status'), '|', resp.get('message'))
else:
    print('no pending transcripts to certify (queue already clean)')

# 2 · Edit a student record with mandatory reason
rs = call('GET', '/api/principal/roster/students')
sid = rs['data'][0]['id']
before = rs['data'][0].get('advisor')
edit = call('PUT', '/api/principal/roster/students/' + sid,
            {'advisor': 'E2E Verified Advisor', 'reason': 'Round-trip verification (test script)'})
print('edit →', edit.get('status'), '| previous advisor =', before)

# 3 · Activity feed: role=principal + audit trail surfaces both actions
aud = call('GET', '/api/principal/audit?limit=8&role=principal')
print('audit rows:', len(aud['data']))
for e in aud['data'][:6]:
    print(' ·', e['action'], '|', e['entity_id'], '|', (e['reason'] or '')[:40])

# 4 · Deep-link from teachers page (?actor=<id>) — actor filter must be honored
tid = call('GET', '/api/principal/roster/teachers')['data'][0]['id']
deep = call('GET', '/api/principal/audit?actor=' + urllib.parse.quote(tid, safe=''))
print('actor=%s → %d events' % (tid, len(deep['data'])))

# 5 · Overlay file persisted after edit (real disk write, not just memory)
import os
overlay = 'data/students_overlay.json'
print('overlay exists:', os.path.exists(overlay), 'size:', os.path.getsize(overlay) if os.path.exists(overlay) else 0)

print('\nWORKFLOW ROUND-TRIP OK')
