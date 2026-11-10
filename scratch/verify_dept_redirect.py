"""Verify shared departments/department pages: default student view OK,
?portal=teacher redirects to teacher-departments.html, engine hydrated, no errors."""
from playwright.sync_api import sync_playwright

CHECKS = [
    ('http://localhost:3000/pages/shared/departments.html', False),
    ('http://localhost:3000/pages/shared/departments.html?portal=teacher', True),
    ('http://localhost:3000/pages/shared/department.html?dept=english&portal=teacher', True),
    ('http://localhost:3000/pages/shared/department.html?dept=english', False),
]

PROBE = """() => {
  const slots = [...document.querySelectorAll('[data-ngis-icon]')];
  return { engine: !!(window.NGIS && window.NGIS.icon),
           slots: slots.length,
           unhyd: slots.filter(s => !s.querySelector('svg')).length,
           ready: document.body.classList.contains('ready') };
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for url, expect_redirect in CHECKS:
        pg = b.new_context(viewport={'width': 1280, 'height': 800}).new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)[:150]))
        pg.goto(url, wait_until='domcontentloaded')
        pg.wait_for_timeout(1800)
        d = pg.evaluate(PROBE)
        red = 'teacher-departments' in pg.url
        ok = (red == expect_redirect) and d['engine'] and d['unhyd'] == 0 and not errs
        print('%s %s -> %s | %s | errs=%s' % (
            'PASS' if ok else 'FAIL', url.split('3000/')[1],
            'redirected' if red else ' stayed', d, errs[:2]))
        pg.context.close()
    b.close()
