import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        page.on('console', lambda msg: print('CONSOLE:', msg.text))
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        res = await page.evaluate('''() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            const el = document.querySelector('#cardAttendance');
            return {
                match1: el.matches('html[data-theme="dark"] body .hub-card'),
                match2: el.matches('[data-theme="dark"] .hub-card'),
                match3: el.matches('.hub-card'),
                bg: window.getComputedStyle(el).backgroundColor,
                hubCardBgVar: window.getComputedStyle(document.documentElement).getPropertyValue('--hub-card-bg')
            };
        }''')
        print(res)
        await browser.close()

asyncio.run(test())
