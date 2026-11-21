import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Check rows in table
        rows = await page.locator("#dirBody tr").count()
        print(f"Teacher table row count: {rows}")
        
        # Check header columns
        th_count = await page.locator("#dirHead th").count()
        print(f"Header columns count: {th_count}")
        
        # Check no 'Add Teacher' button exists
        add_btn = await page.locator("#btnAddTeacher").count()
        print(f"Add Teacher button count (should be 0): {add_btn}")
        
        # Take screenshot
        await page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/teacher_profiles_table.png")
        print("Screenshot saved to teacher_profiles_table.png")
        
        if errors:
            print(f"Errors detected: {errors}")
        else:
            print("No errors detected!")
            
        await browser.close()

asyncio.run(main())
