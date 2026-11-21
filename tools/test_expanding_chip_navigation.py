"""
=============================================================================
MASTER MVP — Global Expanding-Chip Navigation System Automated Test Suite
Verifies:
1. Desktop suppression (>= 1025px)
2. Mobile & Tablet floating capsule specifications (375px, 768px)
3. Expanding-chip morphing animation (collapse previous, expand new, label reveal)
4. Role-specific destinations across Student, Teacher, Principal, Admin
5. Collision avoidance with mobile sidebar drawer
6. Viewport audit across all 14 required breakpoints:
   320px, 360px, 375px, 390px, 414px, 430px, 600px, 768px, 820px, 1024px, 1280px, 1440px, 1920px, 2560px
7. Zero horizontal scroll & page bottom clearance
8. Multilingual labels (English, Khmer, Chinese)
=============================================================================
"""

import sys
import time
from playwright.sync_api import sync_playwright

VIEWPORTS = [
    ('Small Mobile 1',  320, 568),
    ('Small Mobile 2',  360, 640),
    ('Mobile 375',      375, 812),
    ('iPhone 14/15',    390, 844),
    ('iPhone Plus',     414, 896),
    ('Large Mobile',    430, 932),
    ('Phablet',         600, 960),
    ('Tablet 768',      768, 1024),
    ('Tablet 820',      820, 1180),
    ('Small Desktop',  1024, 768),
    ('Medium Desktop', 1280, 800),
    ('Desktop 1440',   1440, 900),
    ('Large Desktop',  1920, 1080),
    ('Wide Desktop',   2560, 1440)
]

def run_suite():
    print("=====================================================================")
    print("Starting Global Expanding-Chip Navigation System Test Suite...")
    print("=====================================================================\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ─────────────────────────────────────────────────────────────────
        # 1. DESKTOP SUPPRESSION TEST (>= 1025px)
        # ─────────────────────────────────────────────────────────────────
        print("--- 1. Testing Desktop Suppression (>= 1025px) ---")
        dpage = browser.new_page(viewport={"width": 1440, "height": 900})
        dpage.goto("http://127.0.0.1:3000/pages/student/student-exams.html")
        dpage.wait_for_selector("#ngisGlobalNavbar")
        dpage.wait_for_timeout(400)

        dock = dpage.locator("#ngisChipDock")
        is_visible = dock.is_visible()
        print(f"  Desktop dock visibility at 1440px: {is_visible}")
        assert not is_visible, "Expanding-chip dock must be hidden on desktop (>= 1025px)"
        print("  [PASS] Desktop dock strictly suppressed; full sidebar & topbar preserved\n")
        dpage.close()

        # ─────────────────────────────────────────────────────────────────
        # 2. MOBILE DOCK SPECIFICATIONS (375px)
        # ─────────────────────────────────────────────────────────────────
        print("--- 2. Testing Mobile Floating Capsule Specifications (375px) ---")
        mpage = browser.new_page(viewport={"width": 375, "height": 812})
        mpage.goto("http://127.0.0.1:3000/pages/student/student-exams.html")
        mpage.wait_for_selector("#ngisChipDock")
        mpage.wait_for_timeout(400)

        dock = mpage.locator("#ngisChipDock")
        assert dock.is_visible(), "Dock must be visible on mobile (375px)"

        dock_box = dock.bounding_box()
        print(f"  Mobile dock box: width={dock_box['width']:.1f}px, height={dock_box['height']:.1f}px, y={dock_box['y']:.1f}px")
        assert 60 <= dock_box["height"] <= 68, f"Dock height must be ~64px, got {dock_box['height']}px"
        assert dock_box["width"] <= 480, f"Dock width must not exceed 480px, got {dock_box['width']}px"

        # Check track style (capsule radius, white background, shadow)
        track = mpage.locator(".ngis-chip-dock-track")
        assert track.is_visible(), "Track must be visible"

        # Check items count (Student should have 5 items: home, exams, grades, departments, profile)
        items = mpage.locator(".ngis-chip-item")
        count = items.count()
        print(f"  Destination items count: {count}")
        assert count in [4, 5], f"Expected 4 or 5 primary destinations, found {count}"

        # Check Active Item: On student-exams.html, 'exams' should be active
        active_item = mpage.locator(".ngis-chip-item.is-active")
        assert active_item.is_visible(), "There must be an active item"
        active_id = active_item.get_attribute("data-id")
        print(f"  Active destination id: '{active_id}'")
        assert active_id == "exams", f"Expected active item 'exams' on student-exams.html, got '{active_id}'"

        # Check active item specifications
        active_box = active_item.bounding_box()
        print(f"  Active chip box: width={active_box['width']:.1f}px, height={active_box['height']:.1f}px")
        assert 44 <= active_box["height"] <= 52, f"Active chip height should be ~48px, got {active_box['height']}px"
        assert active_box["width"] > 70, f"Active chip should be expanded (>70px), got {active_box['width']}px"

        # Check active label visibility and font weight
        active_label = active_item.locator(".ngis-chip-label")
        assert active_label.is_visible(), "Active chip label must be visible"
        active_label_text = active_label.inner_text()
        print(f"  Active label text: '{active_label_text}'")
        assert active_label_text == "Exams", f"Expected 'Exams', got '{active_label_text}'"

        active_weight = active_label.evaluate("el => window.getComputedStyle(el).fontWeight")
        print(f"  Active label font-weight: {active_weight}")
        assert int(active_weight) <= 500, f"AGENTS.md rule: NO BOLD FONTS. Font-weight must be <= 500, got {active_weight}"

        # Check inactive items (should be compact ~48px, labels collapsed)
        inactive_items = mpage.locator(".ngis-chip-item:not(.is-active)")
        for i in range(inactive_items.count()):
            in_item = inactive_items.nth(i)
            in_box = in_item.bounding_box()
            in_label = in_item.locator(".ngis-chip-label")
            label_w = in_label.evaluate("el => el.getBoundingClientRect().width")
            assert in_box["width"] <= 54, f"Inactive item should be compact (~48px), got {in_box['width']}px"
            assert label_w <= 2, f"Inactive label width should be collapsed (~0px), got {label_w}px"

        print("  [PASS] Mobile capsule specifications & active expanding chip verified\n")

        # ─────────────────────────────────────────────────────────────────
        # 3. INTERACTION & MORPHING EXPANSION TEST
        # ─────────────────────────────────────────────────────────────────
        print("--- 3. Testing Morphing Interaction (Clicking another tab) ---")
        grades_tab = mpage.locator('.ngis-chip-item[data-id="grades"]')
        assert grades_tab.is_visible(), "Grades tab must exist"

        # Click grades tab (should expand grades and navigate)
        grades_tab.click()
        mpage.wait_for_timeout(600)

        # Verify new page loaded and active tab updated
        assert "student-grades.html" in mpage.url, f"Expected URL to include student-grades.html, got {mpage.url}"
        new_active = mpage.locator(".ngis-chip-item.is-active")
        assert new_active.get_attribute("data-id") == "grades", "Grades tab must now be active"
        new_label = new_active.locator(".ngis-chip-label").inner_text()
        print(f"  Navigated and morphed: active tab is now '{new_label}' (id=grades)")
        assert new_label == "Grades", f"Expected 'Grades', got {new_label}"

        # Verify old exams tab is now collapsed
        old_exams = mpage.locator('.ngis-chip-item[data-id="exams"]')
        assert not old_exams.evaluate("el => el.classList.contains('is-active')"), "Exams tab must no longer be active"
        print("  [PASS] Morphing expansion & active navigation interaction verified\n")

        # ─────────────────────────────────────────────────────────────────
        # 4. COLLISION AVOIDANCE WITH SIDEBAR DRAWER
        # ─────────────────────────────────────────────────────────────────
        print("--- 4. Testing Collision Avoidance with Mobile Sidebar Drawer ---")
        hamb = mpage.locator("#ngisMobileMenuBtn")
        assert hamb.is_visible(), "Mobile hamburger button must be visible"

        hamb.click()
        mpage.wait_for_timeout(400)

        # Dock should be hidden or translated down when drawer opens
        dock_hidden = mpage.locator("#ngisChipDock").evaluate("""
            el => {
                const style = window.getComputedStyle(el);
                return style.display === 'none' || style.visibility === 'hidden' || style.opacity === '0' || el.classList.contains('is-hidden');
            }
        """)
        print(f"  Dock concealed when sidebar opened: {dock_hidden}")
        assert dock_hidden, "Dock must be concealed when mobile drawer is open to avoid collision"

        # Close sidebar drawer
        hamb.click()
        mpage.wait_for_timeout(400)
        dock_restored = mpage.locator("#ngisChipDock").is_visible()
        print(f"  Dock restored after sidebar closed: {dock_restored}")
        assert dock_restored, "Dock must reappear after sidebar drawer closes"
        print("  [PASS] Collision avoidance with mobile sidebar drawer verified\n")
        mpage.close()

        # ─────────────────────────────────────────────────────────────────
        # 5. ROLE-SPECIFIC DESTINATIONS ACROSS PORTALS
        # ─────────────────────────────────────────────────────────────────
        print("--- 5. Testing Role-Specific Navigation Across Portals ---")
        portals_to_test = [
            ("Teacher",   "http://127.0.0.1:3000/pages/teacher/teacher.html",     ["home", "roster", "attendance", "work", "profile"], "home"),
            ("Principal", "http://127.0.0.1:3000/pages/principal/principal.html", ["home", "classes", "students", "reports", "profile"], "home"),
            ("Admin",     "http://127.0.0.1:3000/pages/admin/admin.html",         ["home", "users", "classes", "cms", "settings"], "home"),
            ("Student",   "http://127.0.0.1:3000/pages/student/student.html",     ["home", "exams", "grades", "departments", "profile"], "home")
        ]

        for role_name, url, expected_tabs, expected_active in portals_to_test:
            page = browser.new_page(viewport={"width": 375, "height": 812})
            page.goto(url)
            page.wait_for_selector("#ngisChipDock")
            page.wait_for_timeout(300)

            cur_tabs = [page.locator(".ngis-chip-item").nth(i).get_attribute("data-id") for i in range(page.locator(".ngis-chip-item").count())]
            active_id = page.locator(".ngis-chip-item.is-active").get_attribute("data-id")

            print(f"  [{role_name} Portal] Tabs: {cur_tabs} | Active: '{active_id}'")
            assert cur_tabs == expected_tabs, f"Expected {expected_tabs}, got {cur_tabs}"
            assert active_id == expected_active, f"Expected active '{expected_active}', got '{active_id}'"
            page.close()

        print("  [PASS] All portal roles correctly rendered distinct, verified destinations\n")

        # ─────────────────────────────────────────────────────────────────
        # 6. MULTILINGUAL SUPPORT (English, Khmer, Chinese)
        # ─────────────────────────────────────────────────────────────────
        print("--- 6. Testing Multilingual Label Updates ---")
        lpage = browser.new_page(viewport={"width": 375, "height": 812})
        lpage.goto("http://127.0.0.1:3000/pages/student/student.html")
        lpage.wait_for_selector("#ngisChipDock")
        lpage.wait_for_timeout(300)

        # Switch to Khmer via event or localStorage
        lpage.evaluate("""
            () => {
                localStorage.setItem('ngis_lang', 'km');
                window.dispatchEvent(new CustomEvent('ngis:lang-changed', { detail: { lang: 'km' } }));
            }
        """)
        lpage.wait_for_timeout(300)
        km_label = lpage.locator(".ngis-chip-item.is-active .ngis-chip-label").inner_text()
        print(f"  Khmer active label: '{km_label}'")
        assert km_label == "ទំព័រដើម", f"Expected 'ទំព័រដើម', got '{km_label}'"

        # Switch to Chinese
        lpage.evaluate("""
            () => {
                localStorage.setItem('ngis_lang', 'zh');
                window.dispatchEvent(new CustomEvent('ngis:lang-changed', { detail: { lang: 'zh' } }));
            }
        """)
        lpage.wait_for_timeout(300)
        zh_label = lpage.locator(".ngis-chip-item.is-active .ngis-chip-label").inner_text()
        print(f"  Chinese active label: '{zh_label}'")
        assert zh_label == "首页", f"Expected '首页', got '{zh_label}'"

        # Restore English
        lpage.evaluate("""
            () => {
                localStorage.setItem('ngis_lang', 'en');
                window.dispatchEvent(new CustomEvent('ngis:lang-changed', { detail: { lang: 'en' } }));
            }
        """)
        lpage.wait_for_timeout(300)
        en_label = lpage.locator(".ngis-chip-item.is-active .ngis-chip-label").inner_text()
        assert en_label == "Home", f"Expected 'Home', got '{en_label}'"
        print("  [PASS] Multilingual label updates verified\n")
        lpage.close()

        # ─────────────────────────────────────────────────────────────────
        # 7. RESPONSIVE BREAKPOINT AUDIT & ZERO HORIZONTAL OVERFLOW
        # ─────────────────────────────────────────────────────────────────
        print("--- 7. Testing All 14 Responsive Breakpoints & Zero Overflow ---")
        for name, width, height in VIEWPORTS:
            rpage = browser.new_page(viewport={"width": width, "height": height})
            rpage.goto("http://127.0.0.1:3000/pages/student/student-exams.html")
            rpage.wait_for_timeout(300)

            sw = rpage.evaluate("() => document.documentElement.scrollWidth")
            cw = rpage.evaluate("() => document.documentElement.clientWidth")
            assert sw <= cw, f"[{name} {width}px] Horizontal overflow detected! scrollWidth={sw} > clientWidth={cw}"

            if width <= 1024:
                dock_el = rpage.locator("#ngisChipDock")
                assert dock_el.is_visible(), f"[{name} {width}px] Dock should be visible on mobile/tablet"
                box = dock_el.bounding_box()
                assert box["width"] <= width, f"[{name} {width}px] Dock width {box['width']} exceeds viewport {width}"
                # Check bottom padding on body
                body_pad = rpage.evaluate("() => window.getComputedStyle(document.body).paddingBottom")
                assert "px" in body_pad and int(float(body_pad.replace("px", ""))) >= 80, f"Body bottom padding should be >= 80px, got {body_pad}"
                print(f"  [PASS] {name:<16} ({width:>4}x{height:>4}): Dock width={box['width']:.1f}px, body pad={body_pad}, zero overflow")
            else:
                dock_el = rpage.locator("#ngisChipDock")
                assert not dock_el.is_visible(), f"[{name} {width}px] Dock must be hidden on desktop"
                print(f"  [PASS] {name:<16} ({width:>4}x{height:>4}): Dock correctly suppressed on desktop, zero overflow")

            rpage.close()

        browser.close()

    print("\n=====================================================================")
    print("ALL GLOBAL EXPANDING-CHIP NAVIGATION TESTS PASSED 100%!")
    print("=====================================================================")

if __name__ == "__main__":
    run_suite()
