import asyncio
from playwright.async_api import async_playwright

async def run_tests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        viewports = [
            ("Desktop", 1440, 900),
            ("Laptop", 1024, 768),
            ("Tablet", 768, 1024),
            ("Mobile", 390, 844)
        ]

        base_url = "http://localhost:3000/pages/teacher/teacher-reports.html"

        for vp_name, width, height in viewports:
            context = await browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1
            )
            await context.add_init_script("""
                localStorage.setItem('auth_user', JSON.stringify({
                    id: 'teacher-jenkins',
                    name: 'Dr. Sarah Jenkins',
                    role: 'teacher',
                    email: 'jenkins@ngis.edu'
                }));
                localStorage.setItem('token', 'fake-jwt-token-teacher');
                localStorage.setItem('ngis-theme', 'light');
            """)

            page = await context.new_page()
            await page.goto(base_url, wait_until="networkidle")
            await page.wait_for_timeout(600)

            print(f"\n--- Testing Reports Viewport: {vp_name} ({width}x{height}) ---")

            # 1. Zero horizontal overflow check on root viewport
            scroll_width = await page.evaluate("document.documentElement.scrollWidth")
            inner_width = await page.evaluate("window.innerWidth")
            print(f"Viewport width: {inner_width}, doc scrollWidth: {scroll_width}")
            assert scroll_width <= inner_width + 1, f"Horizontal overflow detected! scrollWidth={scroll_width} > innerWidth={inner_width}"

            # 2. Hamburger button check on mobile/tablet (<= 1024px)
            if width <= 1024:
                hambs = page.locator('[data-action="toggle-sidebar"]')
                count = await hambs.count()
                print(f"Found {count} hamburger buttons")
                assert count > 0, "No hamburger button found with [data-action='toggle-sidebar']"

                visible_hamb = None
                for i in range(count):
                    btn = hambs.nth(i)
                    if await btn.is_visible():
                        visible_hamb = btn
                        break
                assert visible_hamb is not None, "No visible hamburger button found on screen <= 1024px"
                print("Visible hamburger button verified.")

                # Click hamburger to toggle sidebar
                await visible_hamb.click()
                await page.wait_for_timeout(300)
                sidebar = page.locator('#sidebar')
                assert await sidebar.is_visible(), "Sidebar did not become visible after clicking hamburger!"
                print("Sidebar successfully toggled open.")

                # Close sidebar cleanly
                await page.evaluate("window.toggleSidebar ? window.toggleSidebar(false) : null")
                await page.wait_for_timeout(300)

            # 3. Table Rows Render Check (17 students)
            rows = page.locator("#reportsTableBody tr[data-student-id]")
            row_count = await rows.count()
            print(f"Table row count: {row_count}")
            assert row_count == 17, f"Expected 17 student rows, got {row_count}"

            # 4. Preview Modal Check
            # Click preview on row 1 (Nrinphouneta Hok)
            preview_btn = page.locator("#reportsTableBody tr:first-child button:has-text('Preview')")
            await preview_btn.click()
            await page.wait_for_timeout(300)

            modal = page.locator("#modalReportCard")
            assert await modal.is_visible(), "Report preview modal did not open!"
            modal_name = await page.locator("#modalStudentName").inner_text()
            print(f"Modal Student Name: {modal_name}")
            assert "Nrinphouneta Hok" in modal_name, f"Expected Nrinphouneta Hok in modal, got {modal_name}"

            # Close preview modal
            close_btn = page.locator("#modalReportCard button:has-text('Close Preview')").last
            await close_btn.click()
            await page.wait_for_timeout(200)
            assert not await modal.is_visible(), "Modal did not close after clicking Close button"
            print("Modal preview and close verified.")

            # 5. Search Filtering Check
            search_input = page.locator("#searchReportInput")
            await search_input.fill("Emily")
            await page.wait_for_timeout(200)
            filtered_count = await page.locator("#reportsTableBody tr[data-student-id]").count()
            print(f"Filtered count for 'Emily': {filtered_count}")
            assert filtered_count == 1, f"Expected 1 row for Emily, got {filtered_count}"
            row_text = await page.locator("#reportsTableBody tr[data-student-id]:first-child").inner_text()
            assert "Emily Jenkins" in row_text

            # Clear search
            await search_input.fill("")
            await page.wait_for_timeout(200)
            reset_count = await page.locator("#reportsTableBody tr[data-student-id]").count()
            assert reset_count == 17, f"Expected 17 rows after resetting search, got {reset_count}"

            # 6. Publish Action Check
            # Select Virak Heng (row 3, initial status Unpublished)
            virak_checkbox = page.locator("tr[data-student-id='2026-STD-0145'] input[type='checkbox']")
            # Make sure it's checked
            is_checked = await virak_checkbox.is_checked()
            if not is_checked:
                await virak_checkbox.check()
            
            # Click Publish Selected (desktop or mobile header button)
            publish_btn = page.locator("#btnPublishSelected")
            if not await publish_btn.is_visible():
                publish_btn = page.locator("header button[title='Publish Reports']")
            await publish_btn.click()
            await page.wait_for_timeout(200)

            # Check that Virak Heng now has status 'Published'
            virak_row = page.locator("tr:has-text('Virak Heng')")
            virak_text = await virak_row.inner_text()
            assert "Published" in virak_text, "Virak Heng status was not updated to Published!"
            print("Batch publish successfully updated student record.")

            # 7. Strict NO BOLD FONTS rule verification
            max_weight = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('h1, h2, h3, h4, h5, h6, b, strong, th, td, button, span, div, p, input, select');
                    let maxW = 400;
                    for (const el of elements) {
                        const style = window.getComputedStyle(el);
                        const weight = parseInt(style.fontWeight, 10) || 400;
                        if (weight > maxW) {
                            maxW = weight;
                        }
                    }
                    return maxW;
                }
            """)
            print(f"Maximum detected font-weight across page: {max_weight}")
            assert max_weight <= 500, f"Violation of NO BOLD FONTS rule! Found font-weight: {max_weight} > 500"

            print(f"--> Viewport {vp_name} PASSED all tests!")
            await context.close()

        await browser.close()
        print("\nAll Reports viewports passed successfully!")

if __name__ == "__main__":
    asyncio.run(run_tests())
