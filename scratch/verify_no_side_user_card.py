import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        test_urls = [
            ('student', 'http://127.0.0.1:3000/pages/student/student.html'),
            ('teacher', 'http://127.0.0.1:3000/pages/teacher/teacher.html'),
            ('dept', 'http://127.0.0.1:3000/pages/shared/department.html')
        ]
        
        for name, url in test_urls:
            page = await browser.new_page(viewport={'width': 1440, 'height': 900})
            await page.goto(url, wait_until='networkidle')
            await page.wait_for_timeout(600)
            
            card = await page.query_selector('#sideUserCard, .side-user-card')
            print(f'[{name}] sideUserCard present: {card is not None}')
            assert card is None, f"[{name}] sideUserCard should be removed!"
            
            sidebar = await page.query_selector('#sidebar')
            is_visible = await sidebar.is_visible() if sidebar else False
            print(f'[{name}] sidebar visible: {is_visible}')
            
            # Take screenshot of sidebar region
            if sidebar:
                await sidebar.screenshot(path=f'scratch/sidebar_{name}_clean.png')
                print(f'Saved scratch/sidebar_{name}_clean.png')
                
            await page.close()
            
        await browser.close()
        print('All sideUserCard removal checks passed!')

asyncio.run(main())

