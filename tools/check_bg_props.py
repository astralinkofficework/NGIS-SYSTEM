import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.wait_for_timeout(1000)
        
        await page.evaluate('''() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            document.documentElement.classList.add('dark');
        }''')
        await page.wait_for_timeout(300)
        await page.locator('#cardAttendance').hover()
        await page.wait_for_timeout(200)
        
        props = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const cs = window.getComputedStyle(el);
            return {
                bg: cs.background,
                bgColor: cs.backgroundColor,
                bgImage: cs.backgroundImage,
                hubVarEl: cs.getPropertyValue('--hub-card-bg'),
                hubVarDoc: window.getComputedStyle(document.documentElement).getPropertyValue('--hub-card-bg')
            };
        }''')
        print(props)
        await browser.close()

asyncio.run(test())
