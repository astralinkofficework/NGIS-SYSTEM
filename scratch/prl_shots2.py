"""Re-capture remaining principal pages with font-ready waits."""
from playwright.sync_api import sync_playwright
import os

PAGES = ['principal-reports.html', 'principal-timetables.html', 'principal-services.html',
         'principal-lost-found.html', 'principal-activity.html', 'principal-profile.html',
         'principal.html', 'principal-departments.html', 'principal-student-profiles.html']
os.makedirs('scratch/prl_audit', exist_ok=True)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={'width': 1440, 'height': 900})
    pg = ctx.new_page()
    # warm the font cache in this context
    pg.goto('http://localhost:3000/pages/principal/principal-classes.html', wait_until='networkidle')
    for name in PAGES:
        pg.goto('http://localhost:3000/pages/principal/' + name, wait_until='networkidle')
        pg.evaluate("() => document.fonts.ready")
        pg.wait_for_timeout(2200)
        pg.screenshot(path='scratch/prl_audit/' + name.replace('.html', '') + '.png', full_page=False)
        print('shot', name)
    b.close()
