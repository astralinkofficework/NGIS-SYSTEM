import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        
        errors = []
        dialog_messages = []
        page.on("pageerror", lambda err: errors.append(str(err)))
        page.on("dialog", lambda dialog: dialog_messages.append(dialog.message) or asyncio.create_task(dialog.accept()))
        
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-classes.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Test 3-dot button
        first_more_btn = page.locator(".btn-more-class").first
        await first_more_btn.click()
        await page.wait_for_timeout(300)
        
        menu_visible = await page.locator(".class-action-menu").first.is_visible()
        print(f"3-dot action menu visible on click: {menu_visible}")
        
        # Click delete section on first row (which has enrolled > 0)
        delete_btn = page.locator(".btn-menu-delete").first
        await delete_btn.click()
        await page.wait_for_timeout(300)
        
        print(f"Dialog message received: {dialog_messages}")
        
        # Test Add Class modal
        add_btn = page.locator("#btnAddClass")
        await add_btn.click()
        await page.wait_for_timeout(500)
        
        modal_visible = await page.locator("#modalAddClass").is_visible()
        print(f"Add Class modal visible on click: {modal_visible}")
        
        # Close modal
        await page.locator("#btnCloseModal").click()
        await page.wait_for_timeout(300)
        
        if errors:
            print(f"Errors detected: {errors}")
        else:
            print("No errors detected in class management!")
            
        await browser.close()

asyncio.run(main())
