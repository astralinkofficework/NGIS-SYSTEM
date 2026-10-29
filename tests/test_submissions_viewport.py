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

        base_url = "http://localhost:3000/pages/teacher/teacher-submissions.html"

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

            print(f"\n--- Testing Submissions Viewport: {vp_name} ({width}x{height}) ---")

            # 1. Zero horizontal overflow check on viewport
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

                # Close sidebar
                await page.evaluate("window.toggleSidebar ? window.toggleSidebar(false) : null")
                await page.wait_for_timeout(300)

            # 3. Interactive Row Selection & Detail Panel Sync
            # Initial selected student should be Sophea Chan
            drawer_student = await page.locator("#drawerStudentName").inner_text()
            print(f"Initial Drawer Student: {drawer_student}")
            assert drawer_student == "Sophea Chan", f"Expected Sophea Chan in drawer, got {drawer_student}"

            # Click second row (Nrinphouneta Hok)
            second_row_btn = page.locator("#submissionsTableBody tr:nth-child(2) button:has-text('Edit Mark')")
            await second_row_btn.click()
            await page.wait_for_timeout(200)
            updated_drawer_student = await page.locator("#drawerStudentName").inner_text()
            print(f"After selecting row 2, Drawer Student: {updated_drawer_student}")
            assert updated_drawer_student == "Nrinphouneta Hok", f"Expected Nrinphouneta Hok, got {updated_drawer_student}"

            # Select row 1 (Sophea Chan) again
            await page.locator("#submissionsTableBody tr:first-child button:has-text('Review')").click()
            await page.wait_for_timeout(200)

            # 4. Rubric Live Calculation & Save & Publish
            # Change Mathematical Accuracy input
            crit1_input = page.locator("#rubricCrit1")
            await crit1_input.fill("40")
            await page.wait_for_timeout(200)
            score_disp = await page.locator("#drawerFinalScoreDisplay").inner_text()
            print(f"Computed final score with crit1=40: {score_disp}")
            # Rubric: 40 + 34 + 18 = 92 - 5 penalty = 87
            assert score_disp == "87", f"Expected calculated score 87, got {score_disp}"

            # Save & Publish Mark
            save_publish_btn = page.locator("button:has-text('Save & Publish Mark')")
            await save_publish_btn.click()
            await page.wait_for_timeout(200)

            # Check that table row 1 grade is updated to 87
            table_grade = await page.locator("#tableGrade-2026-STD-0144").inner_text()
            print(f"Updated Table Grade for Sophea Chan: {table_grade}")
            assert "87" in table_grade, f"Expected 87 in table grade, got {table_grade}"

            # 5. Search Filter
            search_input = page.locator("#searchStudent")
            await search_input.fill("Nrinphouneta")
            await page.wait_for_timeout(200)
            visible_rows = await page.evaluate("""
                () => {
                    const rows = Array.from(document.querySelectorAll('#submissionsTableBody tr[data-student-id]'));
                    return rows.filter(r => window.getComputedStyle(r).display !== 'none').length;
                }
            """)
            print(f"Rows matching 'Nrinphouneta': {visible_rows}")
            assert visible_rows == 1, f"Search filter failed: expected 1 row, got {visible_rows}"

            # Clear search
            await search_input.fill("")
            await page.wait_for_timeout(200)

            # 6. Typography Constraint: Strict NO BOLD FONTS (AGENTS.md)
            font_weights = await page.evaluate("""
                () => {
                    const elements = document.querySelectorAll('h1, h2, h3, h4, th, td, button, p, span');
                    let maxWeight = 0;
                    let heavyEl = null;
                    elements.forEach(el => {
                        const style = window.getComputedStyle(el);
                        const fw = parseInt(style.fontWeight, 10);
                        if (!isNaN(fw) && fw > maxWeight) {
                            maxWeight = fw;
                            heavyEl = { tag: el.tagName, text: el.textContent.trim().slice(0, 30), weight: fw };
                        }
                    });
                    return { maxWeight, heavyEl };
                }
            """)
            print(f"Max computed font weight: {font_weights['maxWeight']} (Sample: {font_weights['heavyEl']})")
            assert font_weights['maxWeight'] <= 500, f"Violation of NO BOLD FONTS rule: found font-weight {font_weights['maxWeight']} on {font_weights['heavyEl']}"

            print(f"PASS: {vp_name} ({width}x{height}) verified successfully!")
            await context.close()

        await browser.close()
        print("\nALL SUBMISSIONS VIEWPORT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())

