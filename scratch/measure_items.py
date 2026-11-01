import asyncio
from playwright.async_api import async_playwright

async def measure():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/student/student.html", wait_until="networkidle")
        
        item_info = await page.evaluate("""() => {
            const panel = document.querySelector('.ov-inner-panel');
            const items = Array.from(panel.querySelectorAll('.ov-inner-item'));
            const panelStyle = window.getComputedStyle(panel);
            
            return {
                panelDisplay: panelStyle.display,
                panelJustify: panelStyle.justifyContent,
                panelAlign: panelStyle.alignItems,
                panelGap: panelStyle.gap,
                items: items.map(it => {
                    const s = window.getComputedStyle(it);
                    const rect = it.getBoundingClientRect();
                    return {
                        height: rect.height,
                        padding: s.padding,
                        margin: s.margin,
                        flex: s.flex,
                        text: it.innerText.replace(/\\n/g, ' ')
                    };
                })
            };
        }""")
        
        import pprint
        pprint.pprint(item_info)
        await browser.close()

asyncio.run(measure())

