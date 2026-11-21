import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/admin/admin-teacher-profiles.html", wait_until="networkidle")
        await page.wait_for_timeout(1000)
        
        # Click first 'Profile' button
        profile_btn = page.locator("#dirBody button[data-act='view']").first
        await profile_btn.click()
        await page.wait_for_timeout(500)
        
        modal_visible = await page.locator("#profileModal").is_visible()
        print(f"Profile modal visible on click: {modal_visible}")
        
        # Close profile modal via js
        await page.evaluate("window.__ngisCloseProfile()")
        await page.wait_for_timeout(300)
        
        # Click 'Edit' button
        edit_btn = page.locator("#dirBody button[data-act='edit']").first
        await edit_btn.click()
        await page.wait_for_timeout(500)
        
        form_visible = await page.locator("#formModal").is_visible()
        print(f"Form modal visible on click: {form_visible}")
        
        await browser.close()

asyncio.run(main())
