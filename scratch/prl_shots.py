"""Capture all principal pages at 1440x900 for audit."""
from playwright.sync_api import sync_playwright
import os

PAGES = ['principal.html', 'principal-classes.html', 'principal-departments.html',
         'principal-teacher-profiles.html', 'principal-student-profiles.html',
         'principal-timetables.html', 'principal-attendance.html',
         'principal-reports.html', 'principal-services.html',
         'principal-lost-found.html', 'principal-approvals.html',
         'principal-activity.html', 'principal-profile.html']
os.makedirs('scratch/prl_audit', exist_ok=True)

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_context(viewport={'width': 1440, 'height': 900}).new_page()
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)[:120]))
    for name in PAGES:
        errs.clear()
        try:
            pg.goto('http://localhost:3000/pages/principal/' + name, wait_until='domcontentloaded')
            pg.wait_for_timeout(2500)
            pg.screenshot(path='scratch/prl_audit/' + name.replace('.html', '') + '.png')
            print('%-36s shot ok | errs=%d %s' % (name, len(errs), errs[:1]))
        except Exception as e:
            print('%-36s NAV FAIL %s' % (name, str(e)[:100]))
    b.close()
