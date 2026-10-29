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

        base_url = "http://localhost:3000/pages/teacher/teacher-attendance.html"

        for vp_name, width, height in viewports:
            context = await browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=1
            )
            # Pre-authenticate as teacher in localStorage
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
            page.on("console", lambda msg: print(f"PAGE CONSOLE: {msg.text}"))
            page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))
            await page.goto(base_url, wait_until="networkidle")
            await page.wait_for_timeout(600)

            print(f"\n--- Testing Viewport: {vp_name} ({width}x{height}) ---")

            # 1. Zero horizontal overflow check on viewport
            scroll_width = await page.evaluate("document.documentElement.scrollWidth")
            inner_width = await page.evaluate("window.innerWidth")
            print(f"Viewport width: {inner_width}, doc scrollWidth: {scroll_width}")
            assert scroll_width <= inner_width + 1, f"Horizontal overflow detected! scrollWidth={scroll_width} > innerWidth={inner_width}"

            # 2. Hamburger button check on mobile/tablet (<= 1024px)
            if width <= 1024:
                # Find visible hamburger button
                hambs = page.locator('[data-action="toggle-sidebar"]')
                count = await hambs.count()
                print(f"Found {count} hamburger buttons")
                assert count > 0, "No hamburger button found with [data-action='toggle-sidebar']"
                
                # Check visibility of at least one hamburger
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

            # 3. Interactive Matrix Test (Cell Cycling)
            # Find the Friday button for the first student (index 0)
            fri_btn = page.locator("#attendanceSpreadsheetBody tr:first-child td:nth-child(8) button")
            initial_text = await fri_btn.inner_text()
            print(f"Initial student 1 Friday status: {initial_text}")
            await fri_btn.click()
            await page.wait_for_timeout(100)
            new_text = await fri_btn.inner_text()
            print(f"After click, student 1 Friday status: {new_text}")
            expected_next = 'L' if initial_text == 'P' else ('A' if initial_text == 'L' else ('E' if initial_text == 'A' else 'P'))
            assert new_text == expected_next, f"Cycle failed! Expected {expected_next}, got {new_text}"

            # 4. "Mark All Present" Action
            mark_all_btn = page.locator("#btnMarkAllPresent")
            m_count = await mark_all_btn.count()
            print(f"Mark all count: {m_count}")
            if m_count > 0 and await mark_all_btn.is_visible():
                print("Clicking Mark All Present button...")
                await mark_all_btn.click()
                await page.wait_for_timeout(300)
                fri_btn = page.locator("#attendanceSpreadsheetBody tr:first-child td:nth-child(8) button")
                updated_text = await fri_btn.inner_text()
                print(f"Updated student 1 Friday status: {updated_text}")
                assert updated_text == 'P', f"Mark all present failed! Cell has {updated_text}"
                print("'Mark All Present' verified.")

            # 5. Dual View Switcher (Sheet vs Cards)
            cards_btn = page.locator("#btnViewCardsDesk") if width >= 1024 else page.locator("#btnViewCardsMob")
            await cards_btn.click()
            await page.wait_for_timeout(200)
            cards_view = page.locator("#viewModeCards")
            grid_view = page.locator("#viewModeGrid")
            assert await cards_view.is_visible(), "Cards view container is not visible!"
            assert not await grid_view.is_visible(), "Grid view container should be hidden in cards mode!"
            print("Switched to Cards view successfully.")

            # Switch back to Grid view
            grid_btn = page.locator("#btnViewGridDesk") if width >= 1024 else page.locator("#btnViewGridMob")
            await grid_btn.click()
            await page.wait_for_timeout(200)
            assert await grid_view.is_visible(), "Grid view container should be visible again!"
            print("Switched back to Grid view successfully.")

            # 6. Typography Constraint: Strict NO BOLD FONTS (AGENTS.md)
            # Verify font-weight <= 500 on all headings, buttons, and cells
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
        print("\nALL ATTENDANCE VIEWPORT TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
