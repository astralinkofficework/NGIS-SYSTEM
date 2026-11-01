import asyncio
from playwright.async_api import async_playwright

async def run_check():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # Test desktop 1440
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        await page.screenshot(path='scratch/student_desktop_after.png')

        # Test tablet 820
        await page.set_viewport_size({'width': 820, 'height': 1180})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        await page.screenshot(path='scratch/student_tablet_after.png')

        # Test mobile 390
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        await page.screenshot(path='scratch/student_mobile_after.png')

        await browser.close()
        print('Finished screenshots!')

if __name__ == '__main__':
    asyncio.run(run_check())
