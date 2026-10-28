import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(viewport={'width': 1400, 'height': 900})
        page = await context.new_page()
        # Clear storage and cache
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        # Take full screenshot
        await page.screenshot(path='scratch/actual_teacher_rendered.png', full_page=False)
        
        # Also take a clip of just the sidebar
        sidebar = await page.query_selector('#sidebar')
        if sidebar:
            await sidebar.screenshot(path='scratch/actual_sidebar_clip.png')
            print('Sidebar clip captured!')
        else:
            print('Sidebar element NOT found!')
            
        await browser.close()

asyncio.run(main())
