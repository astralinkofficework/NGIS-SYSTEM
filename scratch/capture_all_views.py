import asyncio
from playwright.async_api import async_playwright

async def capture():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        # 1. Student Desktop 1440
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        await page.screenshot(path='scratch/student_desktop_1440.png')

        # 2. Student Tablet 820
        await page.set_viewport_size({'width': 820, 'height': 1180})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        await page.screenshot(path='scratch/student_tablet_820.png')

        # 3. Student Mobile 390
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
        await page.screenshot(path='scratch/student_mobile_390.png')

        # 4. Teacher Desktop 1440
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.screenshot(path='scratch/teacher_desktop_1440.png')

        # 5. Teacher Mobile 390
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher.html', wait_until='networkidle')
        await page.screenshot(path='scratch/teacher_mobile_390.png')

        # 6. Teacher Department Desktop 1440
        await page.set_viewport_size({'width': 1440, 'height': 900})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-departments.html', wait_until='networkidle')
        await page.screenshot(path='scratch/dept_desktop_1440.png')

        # 7. Teacher Department Mobile 390
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto('http://127.0.0.1:3000/pages/teacher/teacher-departments.html', wait_until='networkidle')
        await page.screenshot(path='scratch/dept_mobile_390.png')

        await browser.close()
        print('Captured all views successfully!')

if __name__ == '__main__':
    asyncio.run(capture())

