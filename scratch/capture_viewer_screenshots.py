import asyncio
from playwright.async_api import async_playwright

async def capture():
    artifacts_dir = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        
        # 1. Principal Timetable Viewer - Desktop
        page = await browser.new_page(viewport={'width': 1440, 'height': 960})
        await page.goto('http://127.0.0.1:3000/pages/principal/principal-timetables.html', wait_until='networkidle')
        await page.wait_for_timeout(1000)
        await page.screenshot(path=f"{artifacts_dir}/viewer_desktop.png", full_page=True)
        print("Captured viewer_desktop.png")
        
        # Test search filter
        search_input = await page.query_selector('#viewerSearchInput')
        if search_input:
            await search_input.fill('Math')
            await page.wait_for_timeout(500)
            await page.screenshot(path=f"{artifacts_dir}/viewer_desktop_search.png")
            print("Captured viewer_desktop_search.png")
            
            # Re-query after render
            search_input2 = await page.query_selector('#viewerSearchInput')
            if search_input2:
                await search_input2.fill('')
                await page.wait_for_timeout(500)

        # 2. Principal Timetable Viewer - Mobile
        mobile_page = await browser.new_page(viewport={'width': 390, 'height': 844})
        await mobile_page.goto('http://127.0.0.1:3000/pages/principal/principal-timetables.html', wait_until='networkidle')
        await mobile_page.wait_for_timeout(1000)
        
        # Check hamburger button
        hb = await mobile_page.query_selector('.mobile-appbar [data-action="toggle-sidebar"]')
        hb_visible = await hb.is_visible() if hb else False
        print("Mobile hamburger button visible:", hb_visible)
        
        await mobile_page.screenshot(path=f"{artifacts_dir}/viewer_mobile.png", full_page=False)
        print("Captured viewer_mobile.png")

        # 3. Admin Timetable Viewer - Desktop
        admin_page = await browser.new_page(viewport={'width': 1440, 'height': 960})
        await admin_page.goto('http://127.0.0.1:3000/pages/admin/admin-timetables.html', wait_until='networkidle')
        await admin_page.wait_for_timeout(1000)
        await admin_page.screenshot(path=f"{artifacts_dir}/admin_viewer_desktop.png", full_page=True)
        print("Captured admin_viewer_desktop.png")

        await browser.close()

asyncio.run(capture())
