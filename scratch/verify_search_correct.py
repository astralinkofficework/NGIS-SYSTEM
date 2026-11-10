"""Verify search correctness: query real API names, then search a guaranteed term."""
import json, urllib.request
from playwright.sync_api import sync_playwright

def api(path):
    req = urllib.request.Request('http://localhost:3000' + path)
    req.add_header('Authorization', 'Bearer mock-jwt-token-principal')
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.loads(r.read().decode('utf-8','replace'))

deps = api('/api/departments')
dlist = deps.get('data', deps) if isinstance(deps, dict) else deps
if isinstance(dlist, dict): dlist = dlist.get('departments') or list(dlist.values())[0]
names = [d.get('name','') for d in dlist][:10] if isinstance(dlist, list) else dlist
print('REAL departments:', names)

cls = api('/api/classes')
clist = cls.get('data', cls)
if isinstance(clist, dict): clist = clist.get('classes') or list(clist.values())[0]
cnames = [c.get('name') or c.get('className') or c.get('section','') for c in clist][:10] if isinstance(clist, list) else clist
print('REAL classes:', cnames)

# pick a guaranteed substring from real dept name
probe = (names[0].split()[0] if names and isinstance(names[0], str) and names[0] else 'a')
print('probe dept substring:', repr(probe))

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width':1440,'height':900})
    seed = ctx.new_page(); seed.goto('http://localhost:3000/pages/principal/principal.html', wait_until='domcontentloaded')
    seed.evaluate("()=>{try{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'X',token:'mock-jwt-token-principal'}));}catch(e){}}")
    seed.close()
    p = ctx.new_page(); p.goto('http://localhost:3000/pages/principal/principal-departments.html', wait_until='networkidle'); p.wait_for_timeout(2200)
    def nrows(): return p.evaluate("()=>document.querySelectorAll('tbody tr:not(:has(td[colspan]))').length")
    all0 = nrows()
    p.fill('#deptSearchInput', probe); p.wait_for_timeout(900)
    narrowed = nrows()
    p.fill('#deptSearchInput', 'zzqqxx'); p.wait_for_timeout(900)
    nomatch = nrows()
    print('departments: all=%d probe"%s"=%d nomatch=%d' % (all0, probe, narrowed, nomatch))
    b.close()
