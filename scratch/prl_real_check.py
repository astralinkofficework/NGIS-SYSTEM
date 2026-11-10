"""Live render check on real-data pages: capture + probe row counts + errors."""
from playwright.sync_api import sync_playwright
import os
os.makedirs('scratch/prl_real', exist_ok=True)

PAGES = ['principal-teacher-profiles.html', 'principal-student-profiles.html',
         'principal-approvals.html', 'principal-activity.html',
         'principal-reports.html', 'principal.html']

PROBE = """() => {
  const rows = document.querySelectorAll('tbody tr').length;
  const bodyText = document.body.innerText;
  return {
    rows,
    hasDemo: /demo/i.test(bodyText) && !/Cambridge|MoEYS/i.test(bodyText),
    emptyState: /no .*(match|record|data|found)/i.test(bodyText),
    err: /undefined|NaN|\[object Object\]/i.test(bodyText)
  };
}"""

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()
    pg.goto('http://localhost:3000/pages/principal/principal-classes.html', wait_until='networkidle')
    pg.close()
    for name in PAGES:
        errs = []
        page = ctx.new_page()
        page.on('pageerror', lambda e: errs.append(str(e)[:120]))
        page.goto('http://localhost:3000/pages/principal/' + name, wait_until='networkidle')
        page.evaluate("() => document.fonts.ready")
        page.wait_for_timeout(2500)
        try:
            d = page.evaluate(PROBE)
        except Exception as e:
            d = {'rows': -1, 'err': str(e)[:60]}
        page.screenshot(path='scratch/prl_real/' + name.replace('.html', '') + '.png')
        print('%-34s rows=%-4s errFlag=%-5s empty=%-5s pageerrs=%d %s' % (
            name, d.get('rows'), d.get('err'), d.get('emptyState'), len(errs), errs[:1]))
        page.close()
    b.close()
