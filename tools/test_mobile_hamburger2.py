import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 375, 'height': 812})
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        await page.wait_for_timeout(500)
        
        btn = page.locator('#mobileMainAppbar [data-action="toggle-sidebar"]')
        print('Visible mobile hamburger count:', await btn.count())
        await btn.click()
        await page.wait_for_timeout(400)
        
        drawer = page.locator('.mobile-drawer, #mobileSidebarDrawer, aside, .sidebar')
        print('Drawer found count:', await drawer.count())
        await page.screenshot(path='tools/roadmap_mobile_drawer_open.png')
        await browser.close()
        print('Mobile drawer verified successfully')

asyncio.run(main())
