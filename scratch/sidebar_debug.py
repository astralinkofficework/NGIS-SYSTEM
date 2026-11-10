from playwright.sync_api import sync_playwright

init = """
try {
  localStorage.setItem('ngis_token', 'mock-jwt-token-admin');
  localStorage.setItem('ngis_user', JSON.stringify({role:'admin', portal:'admin'}));
  localStorage.setItem('ngis_active_portal', 'admin');
} catch (e) {}
"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    ctx.add_init_script(init)
    p = ctx.new_page()
    errs = []
    p.on('pageerror', lambda e: errs.append('PAGEERR:' + str(e)[:300]))
    p.on('console', lambda m: errs.append('CONSOLE:' + m.text[:250]) if m.type == 'error' else None)
    p.goto('http://localhost:3000/pages/admin/admin.html', wait_until='domcontentloaded')
    p.wait_for_timeout(2500)
    print('errors:', errs[:8])
    print(p.evaluate("""() => ({
      sidebar: !!document.getElementById('sidebar'),
      bodyClass: document.body.className,
      mains: document.querySelectorAll('.main').length,
      bodyRole: document.body.getAttribute('data-role'),
      pageVar: typeof window.PAGE,
      layoutLoaded: !!document.querySelector('script[src*="layout.js"]'),
    })"""))
    b.close()
