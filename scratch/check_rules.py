import asyncio
from playwright.async_api import async_playwright

async def check_rules():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for page_name, url in [
            ('Student', 'http://127.0.0.1:3000/pages/student/student.html'),
            ('Teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
            ('Principal', 'http://127.0.0.1:3000/pages/principal/principal.html')
        ]:
            page = await browser.new_page(viewport={'width': 390, 'height': 844})
            await page.goto(url, wait_until='domcontentloaded')
            await page.wait_for_timeout(1000)
            
            # Check hamburger
            hb = await page.query_selector('[data-action="toggle-sidebar"]')
            is_vis = await hb.is_visible() if hb else False
            
            # Check font-weight > 500
            heavy_fonts = await page.evaluate('''() => {
                const els = Array.from(document.querySelectorAll('*'));
                return els.filter(el => {
                    const fw = parseInt(getComputedStyle(el).fontWeight, 10);
                    return fw > 500 && el.offsetHeight > 0 && el.textContent.trim().length > 0;
                }).length;
            }''')
            
            print(f'[{page_name}] Mobile hamburger visible: {is_vis}, Heavy fonts count: {heavy_fonts}')
            
        await browser.close()

asyncio.run(check_rules())

