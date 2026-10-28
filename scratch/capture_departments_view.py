import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop View (1400x900)
        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await context.new_page()
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-departments.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/teacher_departments_desktop.png', full_page=False)
        print('Captured teacher_departments_desktop.png')
        
        # Capture sidebar clip to verify Class Resources is active
        sidebar = await page.query_selector('#sidebar')
        if sidebar:
            await sidebar.screenshot(path='scratch/teacher_departments_sidebar.png')
            print('Captured teacher_departments_sidebar.png')
        await context.close()

        # 2. Mobile View (390x844)
        context = await browser.new_context(viewport={'width': 390, 'height': 844})
        page = await context.new_page()
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-departments.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        await page.screenshot(path='scratch/teacher_departments_mobile.png', full_page=False)
        print('Captured teacher_departments_mobile.png')
        
        # Open mobile drawer via hamburger button
        h_btn = await page.query_selector('header .mobile-hamburger-btn')
        if h_btn:
            await h_btn.click()
            await page.wait_for_timeout(500)
            await page.screenshot(path='scratch/teacher_departments_mobile_drawer.png', full_page=False)
            print('Captured teacher_departments_mobile_drawer.png')
        await context.close()

        await browser.close()

asyncio.run(main())
