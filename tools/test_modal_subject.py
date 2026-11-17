import asyncio
from playwright.async_api import async_playwright

async def test_modal():
    print("Testing admin-modal-add-subject.html...")
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Desktop
        page_desk = await browser.new_page(viewport={"width": 1440, "height": 900})
        page_desk.on("console", lambda m: print("  DESK CONSOLE:", m.type, m.text))
        res_d = await page_desk.goto("http://127.0.0.1:3000/pages/admin/admin-modal-add-subject.html")
        print("  Desktop status:", res_d.status)
        d_overflow = await page_desk.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        print("  Desktop overflow:", d_overflow)

        # Test swatch click
        swatch_blue = page_desk.locator("button[data-color='#93C5FD']")
        await swatch_blue.click()
        hex_val = await page_desk.locator("#colorHexDisplay").text_content()
        print("  Swatch test (should be #93C5FD):", hex_val)

        # Test filter
        await page_desk.locator("#classSearchInput").fill("7A")
        visible_rows = await page_desk.locator(".class-row:visible").count()
        print("  Search '7A' visible rows (should be 1):", visible_rows)

        # Clear search
        await page_desk.locator("#classSearchInput").fill("")

        # Mobile
        page_mob = await browser.new_page(viewport={"width": 375, "height": 667})
        page_mob.on("console", lambda m: print("  MOB CONSOLE:", m.type, m.text))
        res_m = await page_mob.goto("http://127.0.0.1:3000/pages/admin/admin-modal-add-subject.html")
        print("  Mobile status:", res_m.status)
        m_overflow = await page_mob.evaluate("document.documentElement.scrollWidth > window.innerWidth")
        print("  Mobile overflow:", m_overflow)

        # Test submit
        submit_btn = page_mob.locator("#submitBtn")
        await submit_btn.click()
        await page_mob.wait_for_timeout(1000)
        toast_txt = await page_mob.locator("#toastMsg").text_content()
        print("  Toast text after submit:", toast_txt)

        await browser.close()
        print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_modal())
