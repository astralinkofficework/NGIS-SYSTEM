import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # Test 1: Mobile 375px
        page_m = await browser.new_page(viewport={'width': 375, 'height': 812})
        await page_m.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        await page_m.wait_for_timeout(500)
        await page_m.screenshot(path='tools/roadmap_mobile_375.png', full_page=True)
        print('Mobile 375px screenshot taken')
        
        # Test 2: Tablet 768px
        page_t = await browser.new_page(viewport={'width': 768, 'height': 1024})
        await page_t.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        await page_t.wait_for_timeout(500)
        await page_t.screenshot(path='tools/roadmap_tablet_768.png', full_page=True)
        print('Tablet 768px screenshot taken')
        
        # Test 3: Dark Mode
        page_d = await browser.new_page(viewport={'width': 1200, 'height': 800})
        await page_d.goto('http://127.0.0.1:3000/pages/student/student-exams.html')
        await page_d.wait_for_timeout(500)
        await page_d.evaluate("""() => {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('ngis-theme', 'dark');
        }""")
        await page_d.wait_for_timeout(300)
        await page_d.screenshot(path='tools/roadmap_dark_mode.png', full_page=True)
        print('Dark mode screenshot taken')
        
        # Test 4: Search filter interaction
        await page_d.fill('#roadmapFilter', 'Math')
        await page_d.wait_for_timeout(300)
        count = await page_d.locator('.exw-timeline-item').count()
        badge_text = await page_d.locator('#roadmapQueuedBadge').inner_text()
        print('Filtered for Math: items=' + str(count) + ', badge=' + badge_text.strip())
        
        # Test 5: Click to view exam details modal
        await page_d.click('.exw-roadmap-row')
        await page_d.wait_for_timeout(400)
        modal_visible = await page_d.locator('.exw-modal-scrim.show').count() > 0
        modal_title = await page_d.locator('.exw-modal-title').inner_text() if modal_visible else 'None'
        print('Modal opened: ' + str(modal_visible) + ', title: ' + modal_title)
        
        await browser.close()

asyncio.run(main())
