"""Functional audit v2: precise toolbar search IDs, verify search narrows real data."""
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:3000/pages/principal/'
results = []

# (page, search_selector, query, expect_narrow)
SEARCH_TESTS = [
    ('principal-teacher-profiles.html', '#dirSearch', 'Soph', True),
    ('principal-student-profiles.html', '#dirSearch', 'Bopha', True),
    ('principal-classes.html', '#classSearchInput', 'Grade 11', True),
    ('principal-departments.html', '#deptSearchInput', 'Science', True),
    ('principal-attendance.html', '#attSearchInput', 'Sophea', True),
    ('principal-reports.html', '#tableSearch', 'Mathematics', True),
    ('principal-approvals.html', '#searchInput', 'zzzznomatch', True),
    ('principal-services.html', '#serviceSearchInput', 'zzzznomatch', True),
    ('principal-lost-found.html', '#lfSearchInput', 'calculator', True),
    ('principal-timetables.html', '#timetableSearchInput', 'Grade 11', True),
]

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    seed = ctx.new_page(); seed.goto(BASE + 'principal.html', wait_until='domcontentloaded')
    seed.evaluate("""()=>{try{localStorage.setItem('ngis_user',JSON.stringify({id:'PRN-2024-002',role:'principal',name:'Dr. Ly Bunheng',token:'mock-jwt-token-principal'}));}catch(e){}}""")
    seed.close()

    def count(p):
        return p.evaluate("""()=>{
          const tb=[...document.querySelectorAll('tbody')].find(t=>t.querySelector('td')&&!/colspan/.test(t.innerHTML.slice(0,120)));
          let n=document.querySelectorAll('tbody tr').length;
          const empty=document.querySelector('tbody tr td[colspan]');
          if(empty&&/no |match|not found|empty/i.test(empty.textContent)) n=0;
          return n;
        }""")

    for page, sel, q, expect in SEARCH_TESTS:
        p = ctx.new_page(); errs = []
        p.on('pageerror', lambda e: errs.append(str(e)[:90]))
        p.goto(BASE + page, wait_until='networkidle')
        p.wait_for_timeout(2200)
        before = count(p)
        try:
            p.fill(sel, q)
            p.wait_for_timeout(1000)
        except Exception as e:
            results.append((page, 'FILL_FAIL', str(e)[:40], len(errs))); p.close(); continue
        after = count(p)
        ok = (after < before) if expect else True
        results.append((page.replace('principal-','').replace('.html',''), 'before=%d after=%d' % (before, after), 'NARROW' if ok else 'NO-CHANGE', len(errs)))
        p.close()

    b.close()

print('\n%-22s %-20s %-12s errs' % ('PAGE', 'rows', 'verdict'))
for r in results:
    print('%-22s %-20s %-12s %s' % r)
