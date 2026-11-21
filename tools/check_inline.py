import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        res = await page.evaluate('''() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            const el = document.querySelector('#cardAttendance');
            
            // Check inline style attribute
            const inlineBg = el.style.background || el.style.backgroundColor;
            
            return {
                inlineBg: inlineBg,
                computedBg: window.getComputedStyle(el).backgroundColor
            };
        }''')
        print(res)
        await browser.close()

asyncio.run(test())
