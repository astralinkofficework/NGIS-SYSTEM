import asyncio, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1440, 'height': 900})
        errs = []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        await pg.goto('http://127.0.0.1:3000/pages/admin/admin.html', wait_until='networkidle')
        inp = pg.locator('#htbSearchInput')
        print('search input found:', await inp.count())
        await inp.click()
        await pg.keyboard.press('Control+k')
        await pg.wait_for_timeout(300)
        panel_inp = pg.locator('#hpdSearchInput')
        if await panel_inp.count():
            await pg.evaluate("""() => { const i = document.getElementById('hpdSearchInput');
                i.value = 'Kosal'; i.dispatchEvent(new Event('input', { bubbles: true })); }""")
        else:
            await inp.type('Kosal', delay=40)
        await pg.wait_for_timeout(700)
        panel = pg.locator('#htbSearchResults')
        vis = await panel.count()
        links = await pg.locator('#htbSearchResults a').count()
        hrefs = await pg.evaluate("[...document.querySelectorAll('#htbSearchResults a')].map(a => a.getAttribute('href'))")
        print('results panel present:', vis, '| result links:', links, '| hrefs:', hrefs[:3])
        if links:
            await pg.locator('#htbSearchResults a').first.click()
            await pg.wait_for_load_state('networkidle')
            print('clicked first result ->', pg.url.split('3000')[-1], '| rows:', await pg.locator('table tbody tr').count())
        print('page errors:', errs or 'NONE')
        await b.close()

asyncio.run(main())
