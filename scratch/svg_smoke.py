"""Playwright smoke test for the global SVG action-icon system.

For each portal page it verifies:
  - the engine (window.NGIS) loaded,
  - data-ngis-icon slots hydrated to inline <svg>,
  - leftover icon-font glyphs normalised to .ngis-icon-inline svg,
  - the sidebar/nav icons were NOT touched (still font glyphs),
  - no JS console errors.
Saves a screenshot per page and prints a table.
"""
import os, json
from playwright.sync_api import sync_playwright

BASE = 'http://localhost:3000/'
OUT = 'scratch/svg_shots'
os.makedirs(OUT, exist_ok=True)

PAGES = [
    'index.html',
    'pages/admin/admin.html',
    'pages/admin/admin-users.html',
    'pages/admin/admin-exams.html',
    'pages/admin/admin-classes.html',
    'pages/principal/principal-approvals.html',
    'pages/principal/principal-timetables.html',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-gradebook.html',
    'pages/student/student-services.html',
    'pages/student/student-calendar.html',
    'pages/student/student-id.html',
    'pages/shared/exams.html',
    'pages/student/student-exams.html',
    'pages/student/student-grades.html',
    'pages/shared/transcript-viewer.html',
    'pages/admin/admin-lifecycle.html',
    'pages/teacher/teacher-submissions.html',
    'pages/principal/principal.html',
]

JS = r"""
() => {
  const slots = [...document.querySelectorAll('[data-ngis-icon]')];
  const hydrated = slots.filter(s => s.querySelector('svg')).length;
  const normalized = document.querySelectorAll('.ngis-icon-inline svg').length;
  // leftover un-normalised material/ph glyphs OUTSIDE the sidebar/nav
  const inShell = el => !!el.closest('#sidebar, .sidebar, [role="navigation"], nav, .bottom-nav, [data-purpose="primary-sidebar"], .hamburger-btn, .mobile-hamburger-btn');
  const allGlyphs = [...document.querySelectorAll('span.material-symbols-outlined, span.material-symbols, i.ph')];
  const leftoverAction = allGlyphs.filter(g => !inShell(g) && (g.textContent||'').trim()
        && g.closest('button, a[href], [role="button"], td, th, .action-group')).length;
  const shellNavIntact = document.querySelectorAll('#sidebar .nav-link-icon, .sidebar .nav-link-icon').length;
  return {
    engine: !!(window.NGIS && window.NGIS.icon),
    slots: slots.length, hydrated, normalized, leftoverAction, shellNavIntact,
    svgs: document.querySelectorAll('svg').length,
  };
}
"""

results = []
with sync_playwright() as pw:
    browser = pw.chromium.launch()
    for path in PAGES:
        ctx = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = ctx.new_page()
        errors = []
        page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
        page.on('pageerror', lambda e: errors.append('PAGEERROR: ' + str(e)))
        url = BASE + path
        try:
            page.goto(url, wait_until='networkidle', timeout=30000)
        except Exception as e:
            page.wait_for_timeout(1500)
        page.wait_for_timeout(2500)  # let deferred engine + async rows settle
        data = page.evaluate(JS)
        data['page'] = path
        data['errors'] = errors[:6]
        results.append(data)
        shot = os.path.join(OUT, path.replace('/', '_').replace('.html', '') + '.png')
        try:
            page.screenshot(path=shot, full_page=False)
        except Exception as e:
            data['shot_error'] = str(e)
        ctx.close()
    browser.close()

print('%-42s %-7s %6s %8s %10s %6s %6s' % ('PAGE', 'engine', 'slots', 'hydrat', 'normlzd', 'left', 'nav'))
ok = True
for r in results:
    flag = ''
    if not r['engine']: flag += ' NO-ENGINE'
    if r['slots'] and r['hydrated'] < r['slots']: flag += ' UNDER-HYDRATE'
    if r['errors']: flag += ' ERR(%d)' % len(r['errors'])
    if flag: ok = False
    print('%-42s %-7s %6d %8d %10d %6d %6d%s' % (
        r['page'], str(r['engine']), r['slots'], r['hydrated'], r['normalized'],
        r['leftoverAction'], r['shellNavIntact'], flag))
    if r['errors']:
        for e in r['errors']:
            print('      ! ', e[:160])
print('\nOVERALL:', 'PASS' if ok else 'REVIEW')
json.dump(results, open(os.path.join(OUT, 'smoke_results.json'), 'w'), indent=2)
