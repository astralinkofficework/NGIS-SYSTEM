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
        
        card = page.locator('#cardAttendance')
        bg_before = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        
        await card.hover()
        await page.wait_for_timeout(200)
        bg_after = await card.evaluate('el => window.getComputedStyle(el).backgroundColor')
        
        print("Before hover:", bg_before)
        print("During hover:", bg_after)
        await browser.close()

asyncio.run(test())
