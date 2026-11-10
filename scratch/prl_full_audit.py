"""Comprehensive Principal audit: visible-row filtering, filters, actions/modals, responsive overflow."""
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:3000/pages/principal/'
PAGES = [
    'principal.html', 'principal-classes.html', 'principal-departments.html',
    'principal-teacher-profiles.html', 'principal-student-profiles.html',
    'principal-timetables.html', 'principal-attendance.html', 'principal-reports.html',
    'principal-services.html', 'principal-lost-found.html', 'principal-approvals.html',
    'principal-activity.html', 'principal-profile.html',
]
VIEWPORTS = [(1920,1080),(1440,900),(1024,768),(768,1024),(390,844),(360,800)]

VIS_ROWS = """()=>{
  const rows=[...document.querySelectorAll('tbody tr')];
  return rows.filter(r=>r.offsetParent!==null && !r.querySelector('td[colspan]')).length;
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width':1440,'height':900})
    seed = ctx.new_page(); seed.goto(BASE+'principal.html', wait_until='domcontentloaded')
    seed.evaluate("""()=>{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'Dr. Ly Bunheng',token:'mock-jwt-token-principal'}));}""")
    seed.close()

    print('=== FUNCTIONAL: tables, filters, actions, modals ===')
    print('%-26s %-6s %-6s %-8s %-8s %s' % ('PAGE','rows','btns','modals','errs','notes'))
    for pg in PAGES:
        p = ctx.new_page(); errs=[]
        p.on('pageerror', lambda e: errs.append(str(e)[:80]))
        p.on('console', lambda m: errs.append('C:'+m.text[:60]) if m.type=='error' else None)
        p.goto(BASE+pg, wait_until='networkidle'); p.wait_for_timeout(2000)
        try: rows = p.evaluate(VIS_ROWS)
        except Exception: rows = p.evaluate("()=>document.querySelectorAll('*[data-purpose],[class*=card]').length")
        nbtn = p.evaluate("()=>document.querySelectorAll('button').length")
        # modals: count elements that look like modals
        nmodal = p.evaluate("()=>document.querySelectorAll('[id*=Modal],[class*=modal],[role=dialog]').length")
        # try open first modal-ish button with Add/New/View/Edit
        note=''
        try:
            btn = p.query_selector("button:has-text('Add'),button:has-text('New'),button:has-text('Create'),button:has-text('Export')")
            if btn:
                btn.click(); p.wait_for_timeout(600)
                vis = p.evaluate("()=>[...document.querySelectorAll('[id*=Modal],[class*=modal],[role=dialog]')].filter(e=>e.offsetParent!==null).length")
                note = 'openBtn->%dmodal'%vis
                p.keyboard.press('Escape'); p.wait_for_timeout(300)
        except Exception as e:
            note='btnfail'
        print('%-26s %-6s %-6s %-8s %-8s %s' % (pg.replace('principal','P').replace('.html',''), rows, nbtn, nmodal, len(errs), note))
        if errs: print('    ERR:', errs[:3])
        p.close()

    print('\n=== RESPONSIVE: horizontal overflow check ===')
    for w,h in VIEWPORTS:
        vctx = b.new_context(viewport={'width':w,'height':h})
        s = vctx.new_page(); s.goto(BASE+'principal.html', wait_until='domcontentloaded')
        s.evaluate("""()=>{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'X',token:'mock-jwt-token-principal'}));}""")
        s.close()
        bad=[]
        for pg in PAGES:
            p = vctx.new_page()
            p.goto(BASE+pg, wait_until='domcontentloaded'); p.wait_for_timeout(1500)
            of = p.evaluate("()=>{const d=document.documentElement;return d.scrollWidth-d.clientWidth;}")
            if of > 2: bad.append('%s+%d'%(pg.replace('principal-','').replace('.html','').replace('principal.html','dash'),of))
            p.close()
        print('%4dx%-4d overflow: %s' % (w,h, ', '.join(bad) if bad else 'NONE'))
        vctx.close()

    b.close()
