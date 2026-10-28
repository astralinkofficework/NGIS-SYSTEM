import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        
        # 1. Desktop - teacher.html (Dashboard active)
        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await context.new_page()
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        sidebar = await page.query_selector('#sidebar')
        if sidebar:
            await sidebar.screenshot(path='scratch/actual_sidebar_clip.png')
            print('Captured teacher.html sidebar clip')
        await context.close()

        # 2. Desktop - teacher-classes.html (My Class active, matching user screenshot)
        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await context.new_page()
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-classes.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        sidebar = await page.query_selector('#sidebar')
        if sidebar:
            await sidebar.screenshot(path='scratch/actual_classes_sidebar_clip.png')
            print('Captured teacher-classes.html sidebar clip')
        await page.screenshot(path='scratch/actual_classes_rendered.png', full_page=False)
        print('Captured teacher-classes.html full view')
        await context.close()

        # 3. Mobile - teacher.html with sidebar opened via hamburger menu
        context = await browser.new_context(viewport={'width': 390, 'height': 844})
        page = await context.new_page()
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        # click hamburger button
        btn = await page.query_selector('[data-action="toggle-sidebar"]')
        if btn:
            await btn.click()
            await page.wait_for_timeout(600)
            await page.screenshot(path='scratch/actual_mobile_sidebar_opened.png', full_page=False)
            print('Captured mobile sidebar opened')
        await context.close()

        await browser.close()

asyncio.run(main())
