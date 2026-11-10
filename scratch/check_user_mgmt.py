import asyncio, sys, filecmp
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
print('root layout.js == assets/js/layout.js:', filecmp.cmp('layout.js', 'assets/js/layout.js', shallow=False))
lay = open('assets/js/layout.js', encoding='utf-8').read()
print('USER MANAGEMENT group present:', 'USER MANAGEMENT' in lay)
print('admin-users href present:', 'pages/admin/admin-users.html' in lay)

from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        # simulate admin session like other tests do
        await pg.goto('http://127.0.0.1:3000/pages/admin/admin.html', wait_until='networkidle')
        await pg.wait_for_timeout(800)
        labels = await pg.evaluate("""() => [...document.querySelectorAll('#sidebar a, aside a, .sidebar a')]
            .map(a => ({t: a.textContent.trim().slice(0,30), h: a.getAttribute('href')}))
            .filter(x => /user|director/i.test(x.t + (x.h||'')))""")
        print('sidebar user-mgmt entries:', labels)
        groups = await pg.evaluate("""() => [...document.querySelectorAll('#sidebar .nav-group-label, #sidebar .sidebar-group-label, aside .nav-group-title')]
            .map(e => e.textContent.trim())""")
        print('sidebar group labels:', groups)
        print('pageerrors:', errs[:3] or 'NONE')
        await pg.screenshot(path='scratch/admin_sidebar_check.png', clip={'x':0,'y':0,'width':340,'height':900})
        await b.close()
asyncio.run(main())
