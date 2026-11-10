import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html")
        await page.wait_for_timeout(2000)

        # Click the edit button of the first teacher
        first_edit = await page.wait_for_selector('[data-act="edit-row"]')
        print("Found edit button:", await first_edit.inner_text())
        await first_edit.click()
        await page.wait_for_timeout(600)

        # Check if the editor is visible
        first_editor = await page.query_selector('.teacher-inline-editor:not(.hidden)')
        print("Editor visible?", first_editor is not None)

        await page.screenshot(path="scratch/profiles_expanded_editor.png", full_page=True)
        print("Screenshot saved")
        await browser.close()

asyncio.run(run())

