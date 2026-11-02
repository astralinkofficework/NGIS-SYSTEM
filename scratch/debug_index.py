import asyncio
from playwright.async_api import async_playwright

async def debug_index():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(500)
        
        info = await page.evaluate('''() => {
            const hb = document.querySelector('[data-action="toggle-sidebar"]');
            const sb = document.getElementById('sidebar');
            const sc = document.getElementById('scrim');
            return {
                hbFound: !!hb,
                hbVisible: hb ? (hb.offsetWidth > 0 && hb.offsetHeight > 0) : false,
                sbFound: !!sb,
                scFound: !!sc
            };
        }''')
        print('Index Debug Info:', info)
        
        # Click hb
        hb = await page.query_selector('[data-action="toggle-sidebar"]')
        await hb.click()
        await page.wait_for_timeout(300)
        
        after_click = await page.evaluate('''() => {
            const sb = document.getElementById('sidebar');
            const sc = document.getElementById('scrim');
            return {
                sbClasses: sb ? sb.className : null,
                scClasses: sc ? sc.className : null,
                bodyClasses: document.body.className
            };
        }''')
        print('After click:', after_click)
        await page.screenshot(path='scratch/index_click_debug.png')
        await browser.close()

asyncio.run(debug_index())

