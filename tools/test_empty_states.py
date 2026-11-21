import os
import sys
from playwright.sync_api import sync_playwright

art_dir = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"
os.makedirs(art_dir, exist_ok=True)

def run_tests():
    print("Starting Global Empty States & Status Design verification suite...")
    passed = 0
    total = 0

    def assert_true(cond, msg):
        nonlocal passed, total
        total += 1
        if cond:
            passed += 1
            print(f"  [PASS] {msg}")
        else:
            print(f"  [FAIL] {msg}")
            sys.exit(1)

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ── Test 1: Desktop 1440px Empty Table ──
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        page.goto("http://127.0.0.1:3000/pages/shared/empty-states-demo.html")
        page.wait_for_selector(".ngis-empty-state-wrap", timeout=8000)

        # Verify Filing Cabinet SVG
        svg = page.locator(".ngis-empty-illustration-svg").first
        assert_true(svg.is_visible(), "Filing Cabinet SVG is visible on desktop")

        # Verify Centering & Colspan
        cell = page.locator(".ngis-empty-cell").first
        colspan = cell.get_attribute("colspan")
        assert_true(colspan == "7", f"Empty cell spans all 7 columns (colspan={colspan})")

        # Verify Heading & Description
        heading = page.locator(".ngis-empty-heading").first.inner_text()
        assert_true("No students yet" in heading, f"Heading matches contextual message: '{heading}'")

        # Verify Action Button for Admin
        admin_btn = page.locator(".ngis-empty-btn").first
        assert_true(admin_btn.is_visible(), "Action button 'Add Student' is visible for Admin")
        assert_true("Add Student" in admin_btn.inner_text(), f"Button text is 'Add Student': '{admin_btn.inner_text()}'")

        # Screenshot Desktop Empty State
        desktop_screenshot = os.path.join(art_dir, "empty_table_filing_cabinet_desktop_1440.png")
        page.locator("section").first.screenshot(path=desktop_screenshot)
        assert_true(os.path.exists(desktop_screenshot), "Captured empty_table_filing_cabinet_desktop_1440.png")

        # ── Test 2: Role-Aware Permission Enforcement (Student Role) ──
        print("\nVerifying Role-Aware Permissions for Student...")
        page.select_option("#demoRoleSelect", "student")
        page.wait_for_timeout(300)

        student_btns = page.locator(".ngis-empty-btn")
        has_admin_btn = False
        count = student_btns.count()
        for i in range(count):
            if "Add Student" in student_btns.nth(i).inner_text():
                has_admin_btn = True
        assert_true(not has_admin_btn, "Administrative action 'Add Student' is HIDDEN from student view")

        # Screenshot Student Restricted Empty State
        student_shot = os.path.join(art_dir, "empty_table_student_restricted.png")
        page.locator("section").first.screenshot(path=student_shot)
        assert_true(os.path.exists(student_shot), "Captured empty_table_student_restricted.png")

        # ── Test 3: Search Empty State (No Results + Clear Filters) ──
        print("\nVerifying Search Empty State...")
        page.click("button[data-state='search']")
        page.wait_for_timeout(300)

        search_heading = page.locator(".ngis-empty-heading").first.inner_text()
        assert_true("No matching results" in search_heading, f"Search empty heading: '{search_heading}'")

        clear_btn = page.locator(".ngis-empty-btn").first
        assert_true("Clear Filters" in clear_btn.inner_text(), f"Clear filters button present: '{clear_btn.inner_text()}'")

        # Test clicking Clear Filters restores populated state
        clear_btn.click()
        page.wait_for_timeout(1000)
        table_rows = page.locator("#demoTableBody tr")
        assert_true(table_rows.count() >= 4, f"Clicking Clear Filters restored populated records (rows={table_rows.count()})")

        # ── Test 4: Missing Individual Values Standard ──
        print("\nVerifying Missing Individual Values Standard...")
        missing_section = page.locator("section").nth(1)
        missing_shot = os.path.join(art_dir, "missing_values_table.png")
        missing_section.screenshot(path=missing_shot)
        assert_true(os.path.exists(missing_shot), "Captured missing_values_table.png")

        # Verify 'Not assigned', 'Not uploaded', 'Not provided', em dash, and numeric 0
        missing_text = missing_section.inner_text()
        assert_true("Not assigned" in missing_text, "Contains 'Not assigned' indicator")
        assert_true("Not uploaded" in missing_text, "Contains 'Not uploaded' indicator")
        assert_true("Not provided" in missing_text, "Contains 'Not provided' indicator")
        assert_true("—" in missing_text or "–" in missing_text or "&mdash;" in missing_text, "Contains neutral em dash indicator")
        assert_true("STD-2026-001" in missing_text, "Preserves valid data without fake values")

        # ── Test 5: Universal Status Indicators (5 Variants) ──
        print("\nVerifying 5 Base Semantic Status Variants...")
        status_section = page.locator("section").nth(2)
        status_shot = os.path.join(art_dir, "status_indicators_5_variants.png")
        status_section.screenshot(path=status_shot)
        assert_true(os.path.exists(status_shot), "Captured status_indicators_5_variants.png")

        # Check all 5 variants
        default_stat = page.locator(".ngis-status--default").first
        processing_stat = page.locator(".ngis-status--processing").first
        success_stat = page.locator(".ngis-status--success").first
        warning_stat = page.locator(".ngis-status--warning").first
        error_stat = page.locator(".ngis-status--error").first

        assert_true(default_stat.is_visible(), "Default (neutral gray) status visible")
        assert_true(processing_stat.is_visible(), "Processing (blue) status visible")
        assert_true(success_stat.is_visible(), "Success (green) status visible")
        assert_true(warning_stat.is_visible(), "Warning (amber) status visible")
        assert_true(error_stat.is_visible(), "Error (red) status visible")

        # Test Live GSAP Status Transition
        print("\nTesting Live GSAP Status Transition...")
        live_btn = page.locator("#btnLiveTransitionDemo")
        live_btn.click()
        page.wait_for_timeout(500)
        new_status = page.locator("#stat_in_review .ngis-status-indicator").first.get_attribute("data-status")
        assert_true(new_status == "approved", f"Status transitioned smoothly to 'approved': '{new_status}'")

        # ── Test 6: Mobile 375px Viewport & Responsive Layout ──
        print("\nVerifying Mobile 375px Viewport & Touch Ergonomics...")
        page_mobile = browser.new_page(viewport={"width": 375, "height": 812})
        page_mobile.goto("http://127.0.0.1:3000/pages/shared/empty-states-demo.html")
        page_mobile.wait_for_selector(".ngis-empty-state-wrap", timeout=5000)

        # Check SVG mobile size
        mobile_svg = page_mobile.locator(".ngis-empty-illustration-svg").first
        box = mobile_svg.bounding_box()
        assert_true(box is not None and box["width"] <= 120, f"SVG scales down on mobile (width={box['width'] if box else 'None'}px)")

        # Verify Mobile Hamburger Button
        hamb = page_mobile.locator(".mobile-hamburger-btn")
        assert_true(hamb.is_visible(), "Mobile hamburger navigation button is visible")

        # Capture Mobile Screenshot
        mobile_shot = os.path.join(art_dir, "empty_table_mobile_375.png")
        page_mobile.screenshot(path=mobile_shot, full_page=False)
        assert_true(os.path.exists(mobile_shot), "Captured empty_table_mobile_375.png")

        # ── Test 7: Production Pages Integration Check ──
        print("\nVerifying Integration on Production Pages...")
        # Admin Classes
        page.goto("http://127.0.0.1:3000/pages/admin/admin-classes.html")
        page.wait_for_selector("#classesTableBody", timeout=5000)
        # Type search query with 0 matches
        page.fill("#classSearchInput", "xyznonexistent999")
        page.wait_for_timeout(300)
        classes_empty_cell = page.locator("#classesTableBody .ngis-empty-cell")
        assert_true(classes_empty_cell.is_visible(), "Admin Classes displays standardized NGIS_EMPTY state on zero search results")

        # Admin News
        page.goto("http://127.0.0.1:3000/pages/admin/admin-news.html")
        page.wait_for_selector("#newsTableTbody", timeout=5000)
        page.fill("#tableSearchInput", "xyznonexistent999")
        page.wait_for_timeout(300)
        news_empty_cell = page.locator("#newsTableTbody .ngis-empty-cell")
        assert_true(news_empty_cell.is_visible(), "Admin News displays standardized NGIS_EMPTY state on zero search results")

        browser.close()

    print(f"\nAll verification tests passed: {passed}/{total} assertions successful!")

if __name__ == "__main__":
    run_tests()
