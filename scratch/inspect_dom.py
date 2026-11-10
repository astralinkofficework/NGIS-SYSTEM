import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-timetables.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        appbar = await page.query_selector('.mobile-appbar')
        print(".mobile-appbar exists:", bool(appbar))
        if appbar:
            vis = await appbar.is_visible()
            html = await page.evaluate("el => el.outerHTML", appbar)
            print("appbar visible:", vis, "HTML:", html[:200])
        else:
            main = await page.query_selector('.main')
            main_html = await page.evaluate("el => el.outerHTML", main)
            print("Main HTML start:", main_html[:300])
            
        await browser.close()

asyncio.run(inspect())

