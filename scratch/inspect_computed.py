import asyncio
from playwright.async_api import async_playwright

async def inspect():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="domcontentloaded")
        await page.wait_for_selector(".dash-overlap")
        await page.wait_for_timeout(500)
        
        info = await page.evaluate("""() => {
            const evPanel = document.querySelector('.ov-inner-panel');
            const evHead = evPanel?.querySelector('.ov-inner-head');
            const items = Array.from(evPanel?.querySelectorAll('.ov-inner-item') || []);
            const dlPanel = document.querySelector('.ov-deadline-panel');
            const dlItems = Array.from(dlPanel?.querySelectorAll('.ov-deadline-item') || []);
            
            return {
                evPanelStyle: {
                    height: evPanel?.getBoundingClientRect().height,
                    computedHeight: window.getComputedStyle(evPanel).height,
                    flex: window.getComputedStyle(evPanel).flex,
                    display: window.getComputedStyle(evPanel).display
                },
                evHeadHeight: evHead?.getBoundingClientRect().height,
                evItems: items.map(it => ({
                    height: it.getBoundingClientRect().height,
                    padding: window.getComputedStyle(it).padding,
                    margin: window.getComputedStyle(it).margin,
                    lineHeight: window.getComputedStyle(it).lineHeight
                })),
                dlPanelStyle: {
                    height: dlPanel?.getBoundingClientRect().height,
                    flex: window.getComputedStyle(dlPanel).flex
                },
                dlItems: dlItems.map(it => ({
                    height: it.getBoundingClientRect().height,
                    padding: window.getComputedStyle(it).padding,
                    margin: window.getComputedStyle(it).margin
                }))
            };
        }""")
        
        import pprint
        pprint.pprint(info)
        await browser.close()

asyncio.run(inspect())

