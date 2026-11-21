import asyncio
from playwright.async_api import async_playwright

async def test():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='domcontentloaded')
        await page.evaluate('''() => {
            localStorage.setItem('theme', 'dark');
            localStorage.setItem('ngis-theme', 'dark');
            document.documentElement.setAttribute('data-theme', 'dark');
            if (window.NGIS && window.NGIS.setTheme) window.NGIS.setTheme('dark');
        }''')
        await page.wait_for_timeout(300)
        card = page.locator('#cardAttendance')
        
        bg_before = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        await card.hover()
        await page.wait_for_timeout(200)
        bg_hover = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        
        print(f"Dark mode: Before hover = {bg_before}, During hover = {bg_hover}")
        await browser.close()

asyncio.run(test())
