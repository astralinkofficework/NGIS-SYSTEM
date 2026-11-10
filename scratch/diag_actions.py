"""Clean diagnosis: real un-converted ACTION glyphs + exams pageerror stack."""
from playwright.sync_api import sync_playwright
BASE = 'http://localhost:3000/'

PROBE = r"""
() => {
  const inShell = el => !!el.closest('#sidebar, .sidebar, [role="navigation"], nav, .bottom-nav, [data-purpose="primary-sidebar"], .hamburger-btn, .mobile-hamburger-btn, .portal-card, .demo-pill');
  const hosts = [...document.querySelectorAll('button, a[href], [role="button"]')];
  const unconv = [];
  for (const h of hosts) {
    const g = h.querySelector('span.material-symbols-outlined, span.material-symbols, i.ph');
    if (!g || inShell(g) || inShell(h)) continue;
    const name = (g.textContent||'').trim();
    if (!name || g.id) continue;
    unconv.push({name, title:h.getAttribute('title')||'', aria:h.getAttribute('aria-label')||'',
                 cls:(h.className||'').slice(0,46), txt:(h.textContent||'').trim().replace(/\s+/g,' ').slice(0,26)});
  }
  return {unconv};
}
"""

PAGES = ['pages/admin/admin.html','pages/principal/principal-approvals.html',
         'pages/principal/principal-timetables.html','pages/shared/exams.html',
         'pages/student/student-exams.html','pages/student/student-services.html']

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for path in PAGES:
        ctx = b.new_context(viewport={'width': 1440, 'height': 900})
        pg = ctx.new_page()
        errs = []
        pg.on('pageerror', lambda e: errs.append((str(e), (e.stack or ''))))
        try:
            pg.goto(BASE + path, wait_until='networkidle', timeout=30000)
        except Exception:
            pg.wait_for_timeout(1500)
        pg.wait_for_timeout(2000)
        d = pg.evaluate(PROBE)
        print('\n#### %s  (real-action unconverted=%d, pageerrors=%d)' % (path, len(d['unconv']), len(errs)))
        for u in d['unconv'][:20]:
            print('   glyph=%-16s title=%-12s aria=%-12s cls=%-30s txt=%s'
                  % (u['name'], u['title'][:12], u['aria'][:12], u['cls'][:30], u['txt']))
        for msg, stack in errs[:2]:
            print('   ERR:', msg[:200])
            print('   STACK:', stack[:260].replace('\n', ' '))
        ctx.close()
    b.close()
