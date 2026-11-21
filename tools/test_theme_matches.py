import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.evaluate('''() => {
            localStorage.setItem('ngis-theme', 'dark');
            localStorage.setItem('theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
            if (window.NGIS && window.NGIS.setTheme) window.NGIS.setTheme('dark');
        }''')
        await page.wait_for_timeout(300)
        res = await page.evaluate('''() => {
            return {
                attr: document.documentElement.getAttribute('data-theme'),
                matchesNotDark: document.documentElement.matches('html:not([data-theme="dark"])'),
                matchesDark: document.documentElement.matches('html[data-theme="dark"]')
            };
        }''')
        print(res)
        await browser.close()

asyncio.run(test())
