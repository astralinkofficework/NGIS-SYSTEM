import asyncio
from playwright.async_api import async_playwright

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 1280, 'height': 850})

        print("--- 1. Testing Principal Portal (Desktop) ---")
        await page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
        await page.wait_for_timeout(1000)

        # Locate Teachers Management button
        tm_btn = page.locator(".nav-subgroup-label:has-text('Teachers Management')")
        assert await tm_btn.count() == 1, "Teachers Management button not found on Principal page!"
        print("PASS: Teachers Management button found in Principal sidebar.")

        # Subgroup container
        tm_group = page.locator(".nav-subgroup[data-subgroup-id='teachers-mgmt-drop']")
        assert await tm_group.count() == 1, "Teachers Management container not found!"

        # Check initial state (should not be expanded on home page)
        is_expanded_initial = await tm_group.evaluate("el => el.classList.contains('expanded')")
        print(f"Initial expanded on home page: {is_expanded_initial}")

        # Click to expand
        await tm_btn.click()
        await page.wait_for_timeout(300)
        is_expanded = await tm_group.evaluate("el => el.classList.contains('expanded')")
        assert is_expanded, "Teachers Management did not expand on click!"
        print("PASS: Teachers Management expanded on click.")

        # Take screenshot of expanded Teachers Management in Principal sidebar
        await page.locator("#sidebar").screenshot(path="principal_sidebar_expanded.png")
        print("Saved principal_sidebar_expanded.png")

        # Verify all 8 sub-items exist
        expected_items = [
            "Teacher Profile",
            "Verify Teacher Update",
            "Teaching Assignment",
            "Homeroom Teacher Assign",
            "Teacher Attendance",
            "Commendation",
            "Discipline",
            "Input Teacher Efforts"
        ]

        sublinks = page.locator(".nav-subgroup[data-subgroup-id='teachers-mgmt-drop'] .nav-sub-link")
        count = await sublinks.count()
        assert count == 8, f"Expected 8 sublinks, got {count}!"
        print(f"PASS: Exactly 8 sublinks found.")

        for i, expected in enumerate(expected_items):
            text = (await sublinks.nth(i).inner_text()).strip()
            assert expected == text, f"Item {i} mismatch: expected '{expected}', got '{text}'"
            print(f"  [{i+1}/8] '{text}' verified.")

        # Check font-weights of all items (Must comply with AGENTS.md: NO BOLD, max 500)
        weights = await page.evaluate('''() => {
            const labels = document.querySelectorAll('.nav-subgroup[data-subgroup-id="teachers-mgmt-drop"] .nav-link-label, .nav-subgroup[data-subgroup-id="teachers-mgmt-drop"] .nav-subgroup-label');
            return Array.from(labels).map(el => ({
                text: el.innerText.trim(),
                weight: parseInt(window.getComputedStyle(el).fontWeight, 10)
            }));
        }''')
        for w in weights:
            assert w['weight'] <= 500, f"Font weight violation! {w['text']} has fontWeight {w['weight']} > 500"
        print("PASS: Font weight compliance verified (all <= 500, NO BOLD).")

        # Click to collapse again
        await tm_btn.click()
        await page.wait_for_timeout(300)
        is_collapsed = not (await tm_group.evaluate("el => el.classList.contains('expanded')"))
        assert is_collapsed, "Teachers Management did not collapse on second click!"
        print("PASS: Teachers Management collapsed on second click.")

        # Navigate to principal-teacher-profiles.html
        print("\n--- 2. Testing Principal Teacher Profiles (Auto-expanded) ---")
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html")
        await page.wait_for_timeout(1000)

        tm_group_prof = page.locator(".nav-subgroup[data-subgroup-id='teachers-mgmt-drop']")
        is_auto_expanded = await tm_group_prof.evaluate("el => el.classList.contains('expanded')")
        assert is_auto_expanded, "Teachers Management should auto-expand on Teacher Profiles page!"
        print("PASS: Teachers Management auto-expanded on principal-teacher-profiles.html.")

        active_sublink = page.locator(".nav-subgroup[data-subgroup-id='teachers-mgmt-drop'] .nav-sub-link.active")
        assert await active_sublink.count() == 1, "Expected 1 active sublink!"
        active_text = (await active_sublink.inner_text()).strip()
        assert active_text == "Teacher Profile", f"Expected active sublink to be 'Teacher Profile', got '{active_text}'"
        print(f"PASS: Active sublink is '{active_text}'.")
        await page.locator("#sidebar").screenshot(path="principal_sidebar_active_profile.png")

        # Navigate to ?view=verify
        print("\n--- 3. Testing Verify Teacher Update Route ---")
        await page.goto("http://127.0.0.1:3000/pages/principal/principal-teacher-profiles.html?view=verify")
        await page.wait_for_timeout(1000)

        active_sublink_verify = page.locator(".nav-subgroup[data-subgroup-id='teachers-mgmt-drop'] .nav-sub-link.active")
        active_verify_text = (await active_sublink_verify.inner_text()).strip()
        assert active_verify_text == "Verify Teacher Update", f"Expected active sublink 'Verify Teacher Update', got '{active_verify_text}'"
        print(f"PASS: Active sublink on ?view=verify is '{active_verify_text}'.")
        await page.locator("#sidebar").screenshot(path="principal_sidebar_active_verify.png")

        print("\n--- 4. Testing Admin Portal ---")
        await page.goto("http://127.0.0.1:3000/pages/admin/admin.html")
        await page.wait_for_timeout(1000)

        admin_tm_btn = page.locator(".nav-subgroup-label:has-text('Teachers Management')")
        assert await admin_tm_btn.count() == 1, "Teachers Management button not found on Admin page!"
        print("PASS: Teachers Management button found in Admin sidebar.")

        await admin_tm_btn.click()
        await page.wait_for_timeout(300)

        admin_sublinks = page.locator(".nav-subgroup[data-subgroup-id='teachers-mgmt-drop'] .nav-sub-link")
        assert await admin_sublinks.count() == 8, "Expected 8 sublinks in Admin sidebar!"
        print("PASS: Exactly 8 sublinks found in Admin sidebar.")
        await page.locator("#sidebar").screenshot(path="admin_sidebar_expanded.png")

        print("\n--- 5. Testing Mobile Drawer (390px) ---")
        await page.set_viewport_size({'width': 390, 'height': 844})
        await page.goto("http://127.0.0.1:3000/pages/principal/principal.html")
        await page.wait_for_timeout(1000)

        # Open mobile drawer via visible hamburger
        hamb = page.locator(".mobile-hamburger-btn:visible, [data-action='toggle-sidebar']:visible").first
        await hamb.click()
        await page.wait_for_timeout(400)

        # Verify sidebar mobile drawer opened
        is_open = await page.locator("#sidebar").evaluate("el => el.classList.contains('open')")
        assert is_open, "Sidebar mobile drawer did not open!"
        print("PASS: Mobile drawer opened.")

        # Toggle Teachers Management in mobile drawer
        mob_tm_btn = page.locator("#sidebar .nav-subgroup-label:has-text('Teachers Management')")
        await mob_tm_btn.click()
        await page.wait_for_timeout(300)
        mob_tm_group = page.locator("#sidebar .nav-subgroup[data-subgroup-id='teachers-mgmt-drop']")
        mob_is_expanded = await mob_tm_group.evaluate("el => el.classList.contains('expanded')")
        assert mob_is_expanded, "Teachers Management did not expand in mobile drawer!"
        print("PASS: Teachers Management expands in mobile drawer.")
        await page.screenshot(path="principal_mobile_drawer_expanded.png")

        # Check for horizontal overflow
        has_overflow = await page.evaluate("() => document.documentElement.scrollWidth > window.innerWidth")
        assert not has_overflow, "Horizontal overflow detected on mobile!"
        print("PASS: No horizontal overflow on mobile viewport.")

        await browser.close()
        print("\nALL VERIFICATIONS PASSED SUCCESSFULLY!")

asyncio.run(verify())

