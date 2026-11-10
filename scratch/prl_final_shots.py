"""Visual confirmation: rewired toolbars + profiles reference, desktop + mobile."""
from playwright.sync_api import sync_playwright
import os
BASE = 'http://localhost:3000/pages/principal/'
OUT = 'scratch/prl_final'
os.makedirs(OUT, exist_ok=True)
PAGES = ['principal-lost-found.html', 'principal-activity.html',
         'principal-teacher-profiles.html', 'principal-approvals.html']
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    s = ctx.new_page(); s.goto(BASE+'principal.html', wait_until='domcontentloaded')
    s.evaluate("()=>{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'Dr. Ly Bunheng',token:'mock-jwt-token-principal'}));}")
    s.close()
    for pg in PAGES:
        p = ctx.new_page()
        p.goto(BASE+pg, wait_until='networkidle'); p.wait_for_timeout(2300)
        p.screenshot(path='%s/%s_desktop.png' % (OUT, pg.replace('.html','')))
        p.close()
    # mobile for the two toolbars
    mctx = b.new_context(viewport={'width': 390, 'height': 844})
    ms = mctx.new_page(); ms.goto(BASE+'principal.html', wait_until='domcontentloaded')
    ms.evaluate("()=>{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'X',token:'mock-jwt-token-principal'}));}")
    ms.close()
    for pg in ['principal-lost-found.html', 'principal-activity.html']:
        p = mctx.new_page(); p.goto(BASE+pg, wait_until='networkidle'); p.wait_for_timeout(2000)
        p.screenshot(path='%s/%s_mobile.png' % (OUT, pg.replace('.html','')))
        p.close()
    b.close()
    print('captured ->', OUT, os.listdir(OUT))
