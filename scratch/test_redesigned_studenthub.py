import asyncio
from playwright.async_api import async_playwright

async def test_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})

        # Track errors
        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        url = "http://127.0.0.1:3000/pages/principal/principal-services.html"
        print(f"Loading {url}...")
        await page.goto(url)
        await page.wait_for_timeout(1000)

        # Check title
        title = await page.title()
        print("Page Title:", title)

        # Check telemetry cards
        cards = await page.locator(".telemetry-card").count()
        print(f"Found {cards} telemetry cards")
        assert cards == 4, f"Expected 4 cards, found {cards}"

        # Check table rows
        rows = await page.locator("#requestRowsBody tr").count()
        print(f"Found {rows} table rows")
        assert rows >= 5, f"Expected at least 5 rows, found {rows}"

        # Check action buttons & SVGs
        action_btns = await page.locator("#requestRowsBody button").count()
        print(f"Found {action_btns} action buttons in table")
        assert action_btns >= 10, f"Expected at least 10 action buttons, found {action_btns}"

        svgs = await page.locator("#requestRowsBody svg").count()
        print(f"Found {svgs} SVGs inside table action buttons")
        assert svgs >= 10, f"Expected at least 10 SVGs, found {svgs}"

        # Take desktop screenshot
        await page.screenshot(path="scratch/studenthub_redesigned_desktop.png")
        await page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/studenthub_redesigned_desktop.png")
        print("Captured studenthub_redesigned_desktop.png")

        # Test search filter
        search_input = page.locator("#searchInput")
        await search_input.fill("projector")
        await page.wait_for_timeout(300)
        filtered_rows = await page.locator("#requestRowsBody tr:visible").count()
        print(f"After search 'projector': {filtered_rows} visible rows")
        assert filtered_rows == 1, f"Expected 1 matching row, found {filtered_rows}"

        # Clear search
        await search_input.fill("")
        await page.wait_for_timeout(300)

        # Test status tabs
        tab_waiting = page.locator("button.status-tab:has-text('Waiting Decision')")
        await tab_waiting.click()
        await page.wait_for_timeout(300)
        waiting_rows = await page.locator("#requestRowsBody tr:visible").count()
        print(f"Waiting tab visible rows: {waiting_rows}")

        # Test opening detail modal
        review_btn = page.locator("#requestRowsBody tr:visible button:has-text('Revision')").first
        view_btn = page.locator("#requestRowsBody tr:visible button[title*='Review Full Dossier']").first
        await view_btn.click()
        await page.wait_for_timeout(500)

        modal_visible = await page.locator("#detailsModal:not(.hidden)").count()
        print(f"Modal opened successfully: {modal_visible == 1}")
        assert modal_visible == 1, "Expected modal to be open"

        # Capture modal screenshot
        await page.screenshot(path="scratch/studenthub_modal_desktop.png")
        await page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/studenthub_modal_desktop.png")
        print("Captured studenthub_modal_desktop.png")

        # Close modal
        close_btn = page.locator("#detailsModal button[title='Close dialog']")
        await close_btn.click()
        await page.wait_for_timeout(300)

        # Mobile viewport test
        await page.set_viewport_size({"width": 375, "height": 812})
        await page.wait_for_timeout(500)

        # Check mobile hamburger menu
        hamburger = page.locator("button.hamburger-btn[data-action='toggle-sidebar']").first
        is_hamburger_visible = await hamburger.is_visible()
        print(f"Mobile hamburger button visible: {is_hamburger_visible}")
        assert is_hamburger_visible, "Mandatory mobile hamburger button must be visible on mobile!"

        # Capture mobile screenshot
        await page.screenshot(path="scratch/studenthub_redesigned_mobile.png")
        await page.screenshot(path="C:/Users/oudom/.gemini/antigravity/brain/8fd19b10-a09a-43d8-a122-cb4a75dc0ff6/studenthub_redesigned_mobile.png")
        print("Captured studenthub_redesigned_mobile.png")

        print("Page error count:", len(errors))
        if errors:
            print("Errors encountered:", errors)
        assert len(errors) == 0, f"Page had JavaScript errors: {errors}"

        await browser.close()
        print("ALL TESTS PASSED WITH 100% SUCCESS!")

asyncio.run(test_page())
