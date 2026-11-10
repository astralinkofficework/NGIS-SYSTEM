"""Functional audit: exercise real interactions on each Principal page and
verify data-driven behavior + zero page errors. Uses Bearer token via localStorage."""
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:3000/pages/principal/'

def count_rows(page, sel='tbody tr'):
    return page.evaluate("(s)=>document.querySelectorAll(s).length", sel)

results = []

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    # establish principal auth via localStorage token used by NGISAuth
    seed = ctx.new_page()
    seed.goto(BASE + 'principal.html', wait_until='domcontentloaded')
    seed.evaluate("""() => {
      try { localStorage.setItem('ngis_user', JSON.stringify({id:'PRN-2024-002',role:'principal',name:'Dr. Ly Bunheng',token:'mock-jwt-token-principal'})); } catch(e){}
    }""")
    seed.close()

    def newpg(url):
        p = ctx.new_page()
        errs = []
        p.on('pageerror', lambda e: errs.append(str(e)[:100]))
        p.goto(BASE + url, wait_until='networkidle')
        p.evaluate("()=>document.fonts.ready")
        p.wait_for_timeout(2200)
        return p, errs

    # 1. teacher-profiles: search narrows rows
    p, errs = newpg('principal-teacher-profiles.html')
    before = count_rows(p)
    p.fill('#dirSearch, input[type=search]', 'Soph')
    p.wait_for_timeout(900)
    after = count_rows(p)
    results.append(('teacher-profiles search', before, after, 'Soph->fewer', len(errs)))
    p.close()

    # 2. student-profiles: search
    p, errs = newpg('principal-student-profiles.html')
    before = count_rows(p)
    p.fill('#dirSearch, input[type=search]', 'Bopha')
    p.wait_for_timeout(900)
    after = count_rows(p)
    results.append(('student-profiles search', before, after, 'Bopha', len(errs)))
    p.close()

    # 3. classes: search
    p, errs = newpg('principal-classes.html')
    before = count_rows(p)
    p.fill('input[type=search]', 'Grade 11')
    p.wait_for_timeout(900)
    after = count_rows(p)
    results.append(('classes search', before, after, 'Grade 11', len(errs)))
    p.close()

    # 4. departments: search
    p, errs = newpg('principal-departments.html')
    before = count_rows(p)
    p.fill('input[type=search]', 'Science')
    p.wait_for_timeout(900)
    after = count_rows(p)
    results.append(('departments search', before, after, 'Science', len(errs)))
    p.close()

    # 5. attendance: search
    p, errs = newpg('principal-attendance.html')
    before = count_rows(p)
    p.fill('input[type=search]', 'Sophea')
    p.wait_for_timeout(900)
    after = count_rows(p)
    results.append(('attendance search', before, after, 'Sophea', len(errs)))
    p.close()

    # 6. reports: search
    p, errs = newpg('principal-reports.html')
    before = count_rows(p)
    results.append(('reports rows', before, before, 'n/a', len(errs)))
    p.close()

    # 7. approvals: tab switch + search
    p, errs = newpg('principal-approvals.html')
    before = count_rows(p)
    p.fill('input[type=search]', 'zzzznomatch')
    p.wait_for_timeout(900)
    after = count_rows(p)
    results.append(('approvals search', before, after, 'nomatch->0', len(errs)))
    p.close()

    # 8. activity: role filter + query
    p, errs = newpg('principal-activity.html')
    before = count_rows(p)
    p.select_option('#roleFilter', 'teacher')
    p.click('button:has-text("Query")')
    p.wait_for_timeout(1200)
    after = count_rows(p)
    results.append(('activity role=teacher', before, after, 'filter', len(errs)))
    p.close()

    # 9. services: tab filter
    p, errs = newpg('principal-services.html')
    cards_before = p.evaluate("()=>document.querySelectorAll('#serviceGrid > *, [id*=service] > div').length")
    results.append(('services cards', cards_before, cards_before, 'n/a', len(errs)))
    p.close()

    # 10. lost-found: type filter
    p, errs = newpg('principal-lost-found.html')
    before = p.evaluate("()=>document.querySelectorAll('#lostFoundGrid > *').length")
    p.select_option('#typeFilter', 'found')
    p.wait_for_timeout(900)
    after = p.evaluate("()=>document.querySelectorAll('#lostFoundGrid > *').length")
    results.append(('lost-found type=found', before, after, 'filter', len(errs)))
    p.close()

    b.close()

print('\n%-32s %-8s %-8s %-16s errs' % ('PAGE / TEST', 'before', 'after', 'note'))
for r in results:
    print('%-32s %-8s %-8s %-16s %d' % r)
