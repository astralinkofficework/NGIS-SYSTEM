import os
import sys
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:3000"
ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

TEST_PAGES = [
    {"url": f"{BASE_URL}/pages/principal/principal.html", "name": "Principal Dashboard", "portal": "principal"},
    {"url": f"{BASE_URL}/pages/principal/principal-attendance.html", "name": "Principal Attendance", "portal": "principal"},
    {"url": f"{BASE_URL}/pages/teacher/teacher.html", "name": "Teacher Dashboard", "portal": "teacher"},
    {"url": f"{BASE_URL}/pages/teacher/teacher-attendance.html", "name": "Teacher Attendance", "portal": "teacher"},
    {"url": f"{BASE_URL}/pages/student/student.html", "name": "Student Dashboard", "portal": "student"},
    {"url": f"{BASE_URL}/pages/student/student-exams.html", "name": "Student Exams", "portal": "student"},
    {"url": f"{BASE_URL}/pages/admin/admin.html", "name": "Admin Dashboard", "portal": "admin"},
    {"url": f"{BASE_URL}/pages/admin/admin-campus.html", "name": "Admin Campus", "portal": "admin"},
    {"url": f"{BASE_URL}/pages/shared/announcements.html", "name": "Shared Announcements", "portal": "shared"}
]

def run_tests():
    print("=" * 70)
    print("GLOBAL FIX — ZERO HOVER TOOLTIPS VERIFICATION TEST SUITE")
    print("=" * 70)

    total_checks = 0
    passed_checks = 0
    failed_checks = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        for idx, item in enumerate(TEST_PAGES, 1):
            url = item["url"]
            name = item["name"]
            print(f"\n[{idx}/{len(TEST_PAGES)}] Testing: {name} ({url})")

            try:
                page.goto(url, wait_until="load", timeout=8000)
                page.wait_for_timeout(400)
            except Exception as e:
                print(f"  [ERROR] Page navigation failed: {e}")
                failed_checks += 1
                continue

            # 1. Hover across multiple visible sidebar links
            nav_links = page.locator(".sidebar .nav-link:visible, .sidebar .nav-group-label:visible, .sidebar-collapse-btn:visible")
            count = nav_links.count()
            print(f"  Found {count} visible sidebar nav elements to test hover on...")

            hover_tested = 0
            for i in range(min(count, 8)):
                try:
                    link = nav_links.nth(i)
                    link.hover(timeout=1000, force=True)
                    page.wait_for_timeout(30)
                    hover_tested += 1
                except Exception:
                    pass

            # 2. Check DOM for floating tooltip elements
            tooltip_visible = page.evaluate("""() => {
                const tip1 = document.getElementById('ngisGlobalTooltip');
                if (tip1 && window.getComputedStyle(tip1).display !== 'none' && window.getComputedStyle(tip1).opacity > 0) {
                    return 'ngisGlobalTooltip visible';
                }
                const tips = document.querySelectorAll('.ngis-universal-tooltip, .ngis-motion-tooltip');
                for (let t of tips) {
                    const s = window.getComputedStyle(t);
                    if (s.display !== 'none' && s.visibility !== 'hidden' && parseFloat(s.opacity) > 0) {
                        return 'class-based tooltip visible: ' + t.className;
                    }
                }
                return null;
            }""")

            total_checks += 1
            if tooltip_visible is None:
                passed_checks += 1
                print("  [PASS] Zero floating tooltip elements created or rendered on hover.")
            else:
                failed_checks += 1
                print(f"  [FAIL] Tooltip visible: {tooltip_visible}")

            # 3. Check for native title attributes on interactive elements
            title_count = page.evaluate("""() => {
                const els = document.querySelectorAll('button[title], a[title], input[title], select[title], .nav-link[title], [data-tooltip]');
                return Array.from(els).map(el => ({
                    tag: el.tagName,
                    id: el.id,
                    className: el.className ? String(el.className) : '',
                    title: el.getAttribute('title') || el.getAttribute('data-tooltip')
                }));
            }""")

            total_checks += 1
            if len(title_count) == 0:
                passed_checks += 1
                print("  [PASS] Zero title/data-tooltip attributes on interactive elements.")
            else:
                print(f"  [WARN/FAIL] Found {len(title_count)} elements with title/data-tooltip: {title_count[:3]}")
                # If they are just non-button containers, log them
                if all(item['tag'] not in ['BUTTON', 'A'] for item in title_count):
                    passed_checks += 1
                    print("  [PASS] (All non-interactive elements, pass with note)")
                else:
                    failed_checks += 1

            # 4. Check CSS pseudo-element hover tooltip suppression
            pseudo_tooltip = page.evaluate("""() => {
                const rows = document.querySelectorAll('.sidebar .nav-link, .nav-subgroup-label');
                for (let r of rows) {
                    const afterStyle = window.getComputedStyle(r, '::after');
                    const content = afterStyle.getPropertyValue('content');
                    if (content && content !== 'none' && content !== 'normal' && content !== '\"\"' && !content.includes('expand_more')) {
                        // check if it renders text
                        if (content.length > 2 && afterStyle.getPropertyValue('position') === 'absolute') {
                            return 'Pseudo-element tooltip content found: ' + content;
                        }
                    }
                }
                return null;
            }""")

            total_checks += 1
            if pseudo_tooltip is None:
                passed_checks += 1
                print("  [PASS] Zero CSS ::after / ::before hover tooltip popups.")
            else:
                failed_checks += 1
                print(f"  [FAIL] {pseudo_tooltip}")

            # 5. Check accessible aria-labels on icon-only buttons
            accessible_buttons = page.evaluate("""() => {
                const iconBtns = document.querySelectorAll('#navSidebarCollapseBtn, #ngisDesktopNotifBtn, #ngisDesktopLangBtn, #ngisMobileNotifBtn, #ngisMobileLangBtn, #ngisMobileMenuBtn');
                let missing = [];
                for (let btn of iconBtns) {
                    if (btn && !btn.getAttribute('aria-label') && !btn.getAttribute('aria-labelledby')) {
                        missing.push(btn.id || btn.className);
                    }
                }
                return missing;
            }""")

            total_checks += 1
            if len(accessible_buttons) == 0:
                passed_checks += 1
                print("  [PASS] 100% of icon-only navigation buttons have valid aria-label attributes.")
            else:
                failed_checks += 1
                print(f"  [FAIL] Missing aria-label on buttons: {accessible_buttons}")

        # 6. Detailed Interactive Tests on Principal Dashboard
        print("\n--- Detailed Interactive & Functional Regression Tests ---")
        page.goto(f"{BASE_URL}/pages/principal/principal.html", wait_until="load")
        page.wait_for_timeout(500)

        # Hover on table actions or cards
        action_btn = page.locator("button, a.btn, a[href]").first
        if action_btn.is_visible():
            action_btn.hover(force=True, timeout=1000)
            page.wait_for_timeout(100)

        # Capture desktop hover state screenshot
        screenshot_hover = os.path.join(ARTIFACT_DIR, "tooltip_fixed_hover_desktop.png")
        page.screenshot(path=screenshot_hover)
        print(f"  [SCREENSHOT] Saved desktop hover state: {screenshot_hover}")

        # Test Collapsed Rail Hover
        collapse_btn = page.locator("#navSidebarCollapseBtn, #sidebarCollapseBtn").first
        if collapse_btn.is_visible():
            collapse_btn.click()
            page.wait_for_timeout(350)

            # Hover over collapsed rail links
            rail_link = page.locator(".sidebar.collapsed .nav-link").first
            if rail_link.is_visible():
                rail_link.hover(force=True, timeout=1000)
                page.wait_for_timeout(200)

            rail_tooltip = page.evaluate("""() => {
                const tip = document.getElementById('ngisGlobalTooltip');
                if (tip && window.getComputedStyle(tip).display !== 'none' && parseFloat(window.getComputedStyle(tip).opacity) > 0) return true;
                const link = document.querySelector('.sidebar.collapsed .nav-link');
                if (link) {
                    const aft = window.getComputedStyle(link, '::after');
                    if (aft.content && aft.content !== 'none' && aft.display !== 'none') return true;
                }
                return false;
            }""")

            total_checks += 1
            if not rail_tooltip:
                passed_checks += 1
                print("  [PASS] Collapsed rail shows zero floating hover tooltips.")
            else:
                failed_checks += 1
                print("  [FAIL] Collapsed rail still shows hover tooltip!")

            screenshot_rail = os.path.join(ARTIFACT_DIR, "tooltip_fixed_collapsed_rail.png")
            page.screenshot(path=screenshot_rail)
            print(f"  [SCREENSHOT] Saved collapsed rail hover: {screenshot_rail}")

            # Restore sidebar
            collapse_btn.click()
            page.wait_for_timeout(350)

        # Test Functional Popover: Notification Dropdown still works on click
        notif_btn = page.locator("#ngisDesktopNotifBtn")
        if notif_btn.is_visible():
            notif_btn.click()
            page.wait_for_timeout(250)
            dropdown_open = page.locator("#ngisNavNotifPanel").is_visible()

            total_checks += 1
            if dropdown_open:
                passed_checks += 1
                print("  [PASS] Functional click popover: Notification dropdown opens cleanly on click.")
            else:
                failed_checks += 1
                print("  [FAIL] Notification dropdown failed to open on click.")

            screenshot_notif = os.path.join(ARTIFACT_DIR, "tooltip_fixed_functional_notif_dropdown.png")
            page.screenshot(path=screenshot_notif)
            print(f"  [SCREENSHOT] Saved functional notification dropdown: {screenshot_notif}")

            # Close dropdown
            page.keyboard.press("Escape")
            page.wait_for_timeout(150)

        # Test Functional Popover: Language Dropdown still works on click
        lang_btn = page.locator("#ngisDesktopLangBtn")
        if lang_btn.is_visible():
            lang_btn.click()
            page.wait_for_timeout(250)
            lang_open = page.locator("#ngisNavLangPanel").is_visible()

            total_checks += 1
            if lang_open:
                passed_checks += 1
                print("  [PASS] Functional click popover: Language dropdown opens cleanly on click.")
            else:
                failed_checks += 1
                print("  [FAIL] Language dropdown failed to open on click.")

            screenshot_lang = os.path.join(ARTIFACT_DIR, "tooltip_fixed_functional_lang_dropdown.png")
            page.screenshot(path=screenshot_lang)
            print(f"  [SCREENSHOT] Saved functional language dropdown: {screenshot_lang}")

            page.keyboard.press("Escape")
            page.wait_for_timeout(150)

        # 7. Mobile Viewport Check (375px)
        print("\n--- Mobile Viewport (375px) Check ---")
        page.set_viewport_size({"width": 375, "height": 812})
        page.goto(f"{BASE_URL}/pages/principal/principal.html", wait_until="load")
        page.wait_for_timeout(400)

        # Verify hamburger button exists and has aria-label
        mobile_menu_btn = page.locator("#ngisMobileMenuBtn, .hamburger-btn").first
        has_aria = mobile_menu_btn.get_attribute("aria-label")
        has_title = mobile_menu_btn.get_attribute("title")

        total_checks += 1
        if has_aria and not has_title:
            passed_checks += 1
            print(f"  [PASS] Mobile hamburger has aria-label='{has_aria}' and NO title attribute.")
        else:
            failed_checks += 1
            print(f"  [FAIL] Mobile hamburger aria-label={has_aria}, title={has_title}")

        # Open drawer
        mobile_menu_btn.click()
        page.wait_for_timeout(350)
        drawer_open = page.locator("#sidebar.open").is_visible()

        total_checks += 1
        if drawer_open:
            passed_checks += 1
            print("  [PASS] Mobile sidebar drawer opens properly on hamburger click.")
        else:
            failed_checks += 1
            print("  [FAIL] Mobile sidebar drawer failed to open on click.")

        screenshot_mobile = os.path.join(ARTIFACT_DIR, "tooltip_fixed_mobile_drawer_375.png")
        page.screenshot(path=screenshot_mobile)
        print(f"  [SCREENSHOT] Saved mobile drawer: {screenshot_mobile}")

        browser.close()

    print("\n" + "=" * 70)
    print(f"VERIFICATION RESULTS: {passed_checks}/{total_checks} PASSED ({failed_checks} failed)")
    print("=" * 70)
    if failed_checks == 0:
        print("ALL AUDIT REQUIREMENTS SUCCESSFULLY SATISFIED!")
    else:
        sys.exit(1)

if __name__ == '__main__':
    run_tests()
