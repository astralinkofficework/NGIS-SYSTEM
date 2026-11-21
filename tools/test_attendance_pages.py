import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        
        # Test admin-attendance.html
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-attendance.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        cards = await page.locator(".grid .bg-surface-container-lowest").count()
        print(f"Attendance KPI cards count: {cards}")
        
        # Test admin-absence-stats.html
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-absence-stats.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        absence_cards = await page.locator(".grid > div").count()
        print(f"Absence stats cards count: {absence_cards}")
        
        if errors:
            print(f"Errors detected: {errors}")
        else:
            print("No errors detected on attendance & absence pages!")
            
        await browser.close()

asyncio.run(main())
