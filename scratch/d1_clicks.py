import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        # 1) admin dashboard -> Open Students Roster button
        await pg.goto('http://127.0.0.1:3000/pages/admin/admin.html', wait_until='networkidle')
        await pg.click('#btnOpenStudentsRoster')
        await pg.wait_for_load_state('networkidle')
        url = pg.url
        rows = await pg.locator('table tbody tr').count()
        active = await pg.evaluate("document.querySelector('.role-pill-btn.bg-white, .role-pill-btn[aria-selected=true], #directoryTitle')?.textContent || document.querySelector('.role-pill-btn')?.className || 'no-pill'")
        print('roster button ->', url.split('3000')[-1], '| table rows:', rows, '| pill/title:', str(active)[:60])
        # 2) admin-campus -> View all teachers link
        await pg.goto('http://127.0.0.1:3000/pages/admin/admin-campus.html?id=sensok', wait_until='networkidle')
        # link lives in the (inactive) teachers tab panel — activate tab first, else force-navigate
        tab = pg.locator('[data-tab="teachers"], .tab-btn:has-text("eachers"), button:has-text("Faculty")').first
        if await tab.count():
            await tab.click(force=True)
            await pg.wait_for_timeout(300)
        await pg.locator('a[href*="role=teachers"]').first.click(force=True, timeout=8000)
        await pg.wait_for_load_state('networkidle')
        print('campus teachers link ->', pg.url.split('3000')[-1], '| rows:', await pg.locator('table tbody tr').count())
        # 3) hero global search on admin page
        await pg.goto('http://127.0.0.1:3000/pages/admin/admin.html', wait_until='networkidle')
        box = pg.locator('#heroSearch, input[type="search"], .htb-search input').first
        if await box.count():
            await box.fill('Sophea')
            await pg.wait_for_timeout(400)
            res = await pg.locator('.htb-search-results a, #heroSearchResults a').count()
            print('hero search results shown:', res)
        # 4) student lost-found detail modal still has claim/matches buttons (no Message Reporter)
        await pg.goto('http://127.0.0.1:3000/pages/student/student-lost-found.html', wait_until='networkidle')
        print('Message Reporter present:', await pg.locator('text=Message Reporter').count())
        print('page errors:', errs or 'NONE')
        await b.close()

asyncio.run(main())
