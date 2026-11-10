import asyncio
from playwright.async_api import async_playwright

async def check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-timetables.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        btns = await page.query_selector_all('[data-action="toggle-sidebar"]')
        print("Buttons found:", len(btns))
        for i, b in enumerate(btns):
            vis = await b.is_visible()
            box = await b.bounding_box()
            tag = await page.evaluate("el => el.outerHTML", b)
            parent = await page.evaluate("el => el.parentElement.outerHTML", b)
            print(f"Btn {i}: visible={vis}, box={box}")
            print(f"Parent: {parent[:120]}")
            
        await browser.close()

asyncio.run(check())

