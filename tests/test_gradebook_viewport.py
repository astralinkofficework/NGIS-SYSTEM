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

        pages_to_test = [
            "http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html",
            "http://127.0.0.1:3000/pages/teacher/teacher-grades.html"
        ]

        for base_url in pages_to_test:
            page_slug = base_url.split("/")[-1]
            print(f"\n==========================================")
            print(f" TESTING URL: {page_slug}")
            print(f"==========================================")

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
                await page.goto(base_url, wait_until="domcontentloaded")
                await page.wait_for_timeout(600)

                print(f"\n--- Testing Gradebook Viewport: {page_slug} on {vp_name} ({width}x{height}) ---")

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
                    await visible_hamb.evaluate("b => b.click()")
                    await page.wait_for_timeout(300)
                    sidebar = page.locator('#sidebar')
                    assert await sidebar.is_visible(), "Sidebar did not become visible after clicking hamburger!"
                    print("Sidebar successfully toggled open.")

                    # Close sidebar
                    await page.evaluate("window.toggleSidebar ? window.toggleSidebar(false) : null")
                    await page.wait_for_timeout(300)

                # 3. Interactive Score Editing & Real-time Calculation
                score_input = page.locator("#gradebookBody tr:first-child input.score-input").first
                initial_score = await score_input.input_value()
                initial_avg = await page.locator("#gradebookBody tr:first-child .student-avg").inner_text()
                print(f"Student 1 Initial Score: {initial_score}, Initial Avg: {initial_avg}")

                # Change score to 10
                await score_input.fill("10")
                await score_input.dispatch_event("input")
                await page.wait_for_timeout(200)
                updated_avg = await page.locator("#gradebookBody tr:first-child .student-avg").inner_text()
                print(f"Student 1 Updated Avg: {updated_avg}")
                assert updated_avg != initial_avg, "Student average failed to recalculate!"
                print("Live score calculation verified.")

                # 4. Search Filter
                search_input = page.locator("#searchStudentInput")
                await search_input.fill("STU-1002")
                await page.wait_for_timeout(200)
                visible_rows = await page.evaluate("""
                    () => {
                        const rows = Array.from(document.querySelectorAll('#gradebookBody tr[data-student-id]'));
                        return rows.filter(r => window.getComputedStyle(r).display !== 'none').length;
                    }
                """)
                print(f"Rows matching search: {visible_rows}")
                assert visible_rows == 1, f"Search filter failed: expected 1 row, got {visible_rows}"

                # Clear search
                await search_input.fill("")
                await page.wait_for_timeout(200)

                # 5. Typography Constraint: Strict NO BOLD FONTS (AGENTS.md)
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
                print(f"Max computed font weight: {font_weights['maxWeight']} (Sample Tag: {font_weights['heavyEl']['tag'] if font_weights['heavyEl'] else 'None'})")
                assert font_weights['maxWeight'] <= 500, f"Violation of NO BOLD FONTS rule: found font-weight {font_weights['maxWeight']} on {font_weights['heavyEl']}"

                print(f"PASS: {vp_name} ({width}x{height}) verified successfully!")
                await context.close()

        await browser.close()
        print("\nALL GRADEBOOK VIEWPORT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
