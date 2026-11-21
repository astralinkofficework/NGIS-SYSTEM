import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("console", lambda msg: errors.append(msg.text) if msg.type == "error" else None)
        
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-class-assignment.html", wait_until="networkidle")
        await page.wait_for_timeout(1500)
        
        # Check rows in the allocation table
        rows_locator = page.locator("table tbody tr")
        initial_count = await rows_locator.count()
        print(f"Initial row count: {initial_count}")
        
        # Find Show More button
        show_more_btn = page.locator("button[data-act='toggle-class-setup-rows']")
        has_btn = await show_more_btn.is_visible()
        print(f"Show More button visible: {has_btn}")
        
        if has_btn:
            btn_text = await show_more_btn.inner_text()
            print(f"Button text before click: {btn_text.strip()}")
            
            # Click to expand
            await show_more_btn.click()
            await page.wait_for_timeout(500)
            
            expanded_count = await rows_locator.count()
            print(f"Expanded row count: {expanded_count}")
            
            btn_text_expanded = await page.locator("button[data-act='toggle-class-setup-rows']").inner_text()
            print(f"Button text after click: {btn_text_expanded.strip()}")
            
            # Click to collapse
            await page.locator("button[data-act='toggle-class-setup-rows']").click()
            await page.wait_for_timeout(500)
            
            collapsed_count = await rows_locator.count()
            print(f"Collapsed row count: {collapsed_count}")
            
        await page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/f0e0db56-cd04-4f51-a7f8-40ba21b43536/teacher_class_assignment.png")
        print("Screenshot saved to teacher_class_assignment.png")
        
        if errors:
            print(f"Errors detected: {errors}")
        else:
            print("No errors detected!")
            
        await browser.close()

asyncio.run(main())
