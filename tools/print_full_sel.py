import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        sel = await page.evaluate('''() => {
            for (let s of document.styleSheets) {
                if (s.href && s.href.includes('design-system.css')) {
                    for (let r of s.cssRules) {
                        if (r.selectorText && r.selectorText.includes('.card:not([style*="background"]):hover')) {
                            return r.selectorText;
                        }
                    }
                }
            }
            return null;
        }''')
        print('Full selector in design-system.css:')
        print(sel)
        await browser.close()

asyncio.run(test())
