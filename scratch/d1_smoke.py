# D1+D2 post-deletion runtime smoke: every touched page renders with zero errors / zero 404s.
import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

BASE = 'http://127.0.0.1:3000'
PAGES = [
    'pages/admin/admin.html',
    'pages/admin/admin-lifecycle.html',
    'pages/admin/admin-campus.html',
    'pages/admin/admin-grades.html',
    'pages/admin/admin-department-detail.html',
    'pages/admin/admin-users.html?role=students',
    'pages/admin/admin-users.html?role=teachers',
    'pages/admin/admin-classes.html',
    'pages/admin/admin-departments.html',
    'pages/admin/admin-timetables.html',
    'pages/teacher/teacher-departments.html',
    'pages/teacher/teacher-gradebook.html?classId=cls-11a',
    'pages/teacher/teacher-roster.html',
    'pages/teacher/teacher-classes.html',
    'pages/teacher/teacher-lessons.html',
    'pages/student/student-services.html',
    'pages/student/student-lost-found.html',
    'pages/principal/principal.html',
    'pages/principal/principal-profile.html',
    'pages/principal/principal-reports.html',
    'pages/shared/departments.html?portal=student',
    'pages-directory.html',
]

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1440, 'height': 900})
        total_err = total_404 = 0
        for path in PAGES:
            errs, notfound = [], []
            def on_err(e, errs=errs): errs.append(str(e))
            def on_resp(r, notfound=notfound):
                if r.status == 404: notfound.append(r.url)
            page.on('pageerror', on_err)
            page.on('response', on_resp)
            try:
                await page.goto(f'{BASE}/{path}', wait_until='networkidle', timeout=25000)
            except Exception as e:
                errs.append(f'NAV: {e}')
            hero = await page.locator('.hero .hero-topbar').count()
            sidebar = await page.locator('#sidebar, .sidebar').first.is_visible() if await page.locator('#sidebar, .sidebar').count() else False
            status = 'OK ' if not errs and not notfound else 'BAD'
            print(f'{status} {path:<52} hero:{hero} sidebar:{sidebar} errs:{len(errs)} 404:{len(notfound)}')
            for e in errs[:2]: print('     ERR', e[:160])
            for u in notfound[:3]: print('     404', u.split(BASE)[-1])
            total_err += len(errs); total_404 += len(notfound)
            page.remove_listener('pageerror', on_err); page.remove_listener('response', on_resp)
        await browser.close()
        print(f'DONE — pages: {len(PAGES)}, pageerrors: {total_err}, 404s: {total_404}')

asyncio.run(main())
