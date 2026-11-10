"""Verify real (non-demo) layer: hit /api/principal/* endpoints and check
they return real data (not demo fixtures, not errors/empty)."""
import json, urllib.request

BASE = 'http://localhost:3000'

def get(path, cookie=None):
    req = urllib.request.Request(BASE + path)
    req.add_header('Authorization', 'Bearer mock-jwt-token-principal')
    if cookie:
        req.add_header('Cookie', cookie)
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            body = r.read().decode('utf-8', 'replace')
            try:
                return r.status, json.loads(body)
            except Exception:
                return r.status, body[:200]
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8', 'replace')[:200]
    except Exception as e:
        return 'ERR', str(e)[:150]

# Auth: demo auth adopts role from ngis_user cookie. Try setting principal.
# First check what auth the endpoints expect.
for path in ['/api/principal/stats', '/api/principal/approvals',
             '/api/principal/audit?limit=5', '/api/principal/roster/teachers',
             '/api/principal/roster/students']:
    st, data = get(path)
    mode = data.get('mode') if isinstance(data, dict) else '?'
    if isinstance(data, dict):
        d = data.get('data')
        if isinstance(d, dict):
            keys = list(d.keys())[:6]
            n = sum(len(v) for v in d.values() if isinstance(v, list))
        elif isinstance(d, list):
            keys = 'list'; n = len(d)
        else:
            keys = '?'; n = 0
    else:
        keys = '?'; n = 0
    print('%-40s status=%s mode=%s keys=%s count=%s' % (path, st, mode, keys, n))
