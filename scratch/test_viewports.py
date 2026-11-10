import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()

        # Set localStorage for auth if needed
        page = await context.new_page()
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html")
        await page.wait_for_timeout(2000)

        # Desktop 1440px
        await page.set_viewport_size({"width": 1440, "height": 900})
        await page.wait_for_timeout(1000)
        await page.screenshot(path="scratch/profiles_desktop_1440.png", full_page=True)
        print("Desktop screenshot captured")

        # Laptop/Tablet 1024px
        await page.set_viewport_size({"width": 1024, "height": 768})
        await page.wait_for_timeout(500)
        await page.screenshot(path="scratch/profiles_laptop_1024.png", full_page=True)
        print("Laptop screenshot captured")

        # Tablet 768px
        await page.set_viewport_size({"width": 768, "height": 1024})
        await page.wait_for_timeout(500)
        await page.screenshot(path="scratch/profiles_tablet_768.png", full_page=True)
        print("Tablet screenshot captured")

        # Mobile 390px
        await page.set_viewport_size({"width": 390, "height": 844})
        await page.wait_for_timeout(500)
        await page.screenshot(path="scratch/profiles_mobile_390.png", full_page=True)
        print("Mobile screenshot captured")

        # Test clicking edit to expand row
        await page.set_viewport_size({"width": 1440, "height": 900})
        first_edit = await page.query_selector('[data-act="edit-row"]')
        if first_edit:
            await first_edit.click()
            await page.wait_for_timeout(600)
            await page.screenshot(path="scratch/profiles_expanded_editor.png")
            print("Expanded editor screenshot captured")

        await browser.close()

asyncio.run(run())

