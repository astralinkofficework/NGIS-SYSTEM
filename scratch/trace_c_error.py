"""Capture the exact stack of the 'c is not defined' error on profiles pages."""
from playwright.sync_api import sync_playwright
BASE = 'http://localhost:3000/pages/principal/'
with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width':1440,'height':900})
    s = ctx.new_page(); s.goto(BASE+'principal.html', wait_until='domcontentloaded')
    s.evaluate("()=>{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'X',token:'mock-jwt-token-principal'}));}")
    s.close()
    for pg in ['principal-teacher-profiles.html','principal-student-profiles.html']:
        p = ctx.new_page()
        logs=[]
        p.on('pageerror', lambda e: logs.append('PAGEERROR: %s\n%s' % (e.message, (e.stack or '')[:600])))
        p.on('console', lambda m: logs.append('CONSOLE[%s]: %s' % (m.type, m.text[:300])) if m.type == 'error' else None)
        p.goto(BASE+pg, wait_until='networkidle'); p.wait_for_timeout(2500)
        print('==== %s (load phase) ====' % pg)
        for l in logs: print(l)
        logs.clear()
        # now click each visible action-ish button
        for label in ['Export','Add','New','View','Manage']:
            try:
                btn = p.query_selector("button:has-text('%s')" % label)
                if btn:
                    btn.click(); p.wait_for_timeout(700)
                    p.keyboard.press('Escape'); p.wait_for_timeout(300)
            except Exception as e:
                logs.append('click %s fail %s' % (label, str(e)[:60]))
        if logs:
            print('---- after clicks ----')
            for l in logs: print(l)
        p.close()
    b.close()
