import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page.wait_for_timeout(500)
        
        info = await page.evaluate('''() => {
            const pageEl = document.querySelector('.page');
            const mainEl = document.querySelector('.main');
            const hubEl = document.querySelector('.hub-content-container');
            const bodyEl = document.body;
            
            return {
                body: {
                    margin: window.getComputedStyle(bodyEl).margin,
                    padding: window.getComputedStyle(bodyEl).padding,
                    width: window.getComputedStyle(bodyEl).width,
                    overflowX: window.getComputedStyle(bodyEl).overflowX
                },
                main: {
                    margin: window.getComputedStyle(mainEl).margin,
                    padding: window.getComputedStyle(mainEl).padding,
                    width: window.getComputedStyle(mainEl).width,
                    marginLeft: window.getComputedStyle(mainEl).marginLeft,
                    box: mainEl.getBoundingClientRect()
                },
                page: {
                    margin: window.getComputedStyle(pageEl).margin,
                    padding: window.getComputedStyle(pageEl).padding,
                    width: window.getComputedStyle(pageEl).width,
                    box: pageEl.getBoundingClientRect()
                },
                hub: {
                    margin: window.getComputedStyle(hubEl).margin,
                    padding: window.getComputedStyle(hubEl).padding,
                    width: window.getComputedStyle(hubEl).width,
                    box: hubEl.getBoundingClientRect()
                }
            };
        }''')
        import pprint
        pprint.pprint(info)
        await browser.close()

asyncio.run(main())

