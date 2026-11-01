import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Desktop
        page = await browser.new_page(viewport={'width': 1280, 'height': 800})
        await page.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page.wait_for_timeout(800)
        await page.screenshot(path='scratch/dept_curr_desktop.png', full_page=True)
        
        # Tablet
        page_tab = await browser.new_page(viewport={'width': 768, 'height': 1024})
        await page_tab.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page_tab.wait_for_timeout(800)
        await page_tab.screenshot(path='scratch/dept_curr_tablet.png', full_page=True)

        # Mobile
        page_mob = await browser.new_page(viewport={'width': 390, 'height': 844})
        await page_mob.goto('http://127.0.0.1:3000/pages/shared/department.html', wait_until='networkidle')
        await page_mob.wait_for_timeout(800)
        await page_mob.screenshot(path='scratch/dept_curr_mobile.png', full_page=True)

        await browser.close()
        print('Captured department screenshots')

asyncio.run(main())

