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
        
        info = await page.evaluate('''() => {
            const el = document.querySelector('#cardAttendance');
            const bgBefore = window.getComputedStyle(el).backgroundColor;
            
            // Remove style[0]
            const s0 = document.querySelectorAll('style')[0];
            s0.remove();
            const bgAfter = window.getComputedStyle(el).backgroundColor;
            
            return { bgBefore, bgAfter };
        }''')
        print(info)
        await browser.close()

asyncio.run(test())
