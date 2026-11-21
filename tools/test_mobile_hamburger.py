import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 375, 'height': 812})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        await page.wait_for_timeout(500)
        
        btn = page.locator('[data-action="toggle-sidebar"]')
        c = await btn.count()
        print('Hamburger count:', c)
        if c > 0:
            await btn.first.click()
            await page.wait_for_timeout(400)
            await page.screenshot(path='tools/roadmap_mobile_sidebar_open.png')
            print('Captured mobile sidebar open')
        await browser.close()

asyncio.run(main())
