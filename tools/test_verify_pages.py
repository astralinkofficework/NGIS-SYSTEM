import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        # Test student verify
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-student-verify.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        title_student = await page.title()
        print(f"Student Verify Page Title: {title_student}")
        
        # Check review buttons or rows
        rows = await page.locator("#studentMgmtRoot table tbody tr").count()
        print(f"Student verify table rows: {rows}")
        
        # Test teacher verify
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-verify.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        title_teacher = await page.title()
        print(f"Teacher Verify Page Title: {title_teacher}")
        
        rows_teacher = await page.locator("#teacherMgmtRoot table tbody tr").count()
        print(f"Teacher verify table rows: {rows_teacher}")
        
        if errors:
            print(f"Errors detected: {errors}")
        else:
            print("No errors detected on verify pages!")
            
        await browser.close()

asyncio.run(main())
