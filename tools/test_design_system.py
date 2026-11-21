import os
import sys
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

def log(msg):
    print(f"[TEST] {msg}")

def assert_true(cond, msg):
    if not cond:
        print(f"  [FAIL] {msg}")
        raise AssertionError(msg)
    print(f"  [PASS] {msg}")

def run_tests():
    with sync_playwright() as p:
        browser = p.chromium.launch()

        # ── 1. Desktop Test on Design System Preview ──
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        log("Loading design system preview at 1440x900...")
        page.goto("http://127.0.0.1:3000/pages/shared/design-system-preview.html", wait_until="networkidle")

        # Capture Desktop Full Page Screenshot
        desktop_shot = os.path.join(ARTIFACT_DIR, "design_system_preview_desktop_1440.png")
        page.screenshot(path=desktop_shot, full_page=True)
        assert_true(os.path.exists(desktop_shot), "Desktop preview screenshot captured")

        # ── 2. Verify Universal Button Sizing System ──
        log("Verifying Universal Button Sizes (Section 06)...")
        btn_sm = page.locator(".btn-sm").first
        box_sm = btn_sm.bounding_box()
        cs_sm = btn_sm.evaluate("el => window.getComputedStyle(el).height")
        assert_true(cs_sm == "36px" or (box_sm and abs(box_sm["height"] - 36) < 1.0), f"Small button height is 36px (computed: {cs_sm})")

        btn_md = page.locator(".btn-md").first
        box_md = btn_md.bounding_box()
        cs_md = btn_md.evaluate("el => window.getComputedStyle(el).height")
        assert_true(cs_md == "40px" or (box_md and abs(box_md["height"] - 40) < 1.0), f"Medium button height is 40px (computed: {cs_md})")

        btn_lg = page.locator(".btn-lg").first
        box_lg = btn_lg.bounding_box()
        cs_lg = btn_lg.evaluate("el => window.getComputedStyle(el).height")
        assert_true(cs_lg == "56px" or (box_lg and abs(box_lg["height"] - 56) < 1.0), f"Large button height is 56px (computed: {cs_lg})")

        # ── 3. Verify Concentric Nested Corner Radii ──
        log("Verifying Concentric Nested Corner Radii (Section 03)...")
        # Outer 24px -> Inner 16px
        outer24 = page.locator(".concentric-container-24").first
        inner16 = outer24.locator(".nested-card").first
        r_outer24 = outer24.evaluate("el => window.getComputedStyle(el).borderRadius")
        r_inner16 = inner16.evaluate("el => window.getComputedStyle(el).borderRadius")
        assert_true(r_outer24 == "24px", f"Outer container radius is 24px (computed: {r_outer24})")
        assert_true(r_inner16 == "16px", f"Concentric inner radius is 16px (computed: {r_inner16})")

        # Outer 20px -> Inner 12px
        outer20 = page.locator(".concentric-container-20").first
        inner12 = outer20.locator(".nested-card").first
        r_outer20 = outer20.evaluate("el => window.getComputedStyle(el).borderRadius")
        r_inner12 = inner12.evaluate("el => window.getComputedStyle(el).borderRadius")
        assert_true(r_outer20 == "20px", f"Outer container radius is 20px (computed: {r_outer20})")
        assert_true(r_inner12 == "12px", f"Concentric inner radius is 12px (computed: {r_inner12})")

        # Outer 16px -> Inner 8px
        outer16 = page.locator(".concentric-card-16").first
        inner8 = outer16.locator(".nested-subcard").first
        r_outer16 = outer16.evaluate("el => window.getComputedStyle(el).borderRadius")
        r_inner8 = inner8.evaluate("el => window.getComputedStyle(el).borderRadius")
        assert_true(r_outer16 == "16px", f"Outer card radius is 16px (computed: {r_outer16})")
        assert_true(r_inner8 == "8px", f"Concentric inner radius is 8px (computed: {r_inner8})")

        # Capture Concentric Radii Screenshot
        concentric_shot = os.path.join(ARTIFACT_DIR, "concentric_radii_spec.png")
        page.locator("#sectionConcentricRadii").screenshot(path=concentric_shot)
        assert_true(os.path.exists(concentric_shot), "Concentric radii artifact screenshot captured")

        # ── 4. Verify Soft Shadow & Elevation Levels ──
        log("Verifying Soft Elevation Levels (Section 09)...")
        elev1 = page.locator(".elevation-1").first.evaluate("el => window.getComputedStyle(el).boxShadow")
        elev2 = page.locator(".elevation-2").first.evaluate("el => window.getComputedStyle(el).boxShadow")
        elev3 = page.locator(".elevation-3").first.evaluate("el => window.getComputedStyle(el).boxShadow")
        elev4 = page.locator(".elevation-4").first.evaluate("el => window.getComputedStyle(el).boxShadow")
        assert_true("none" not in elev1, f"Elevation 1 has soft shadow: {elev1}")
        assert_true("none" not in elev2, f"Elevation 2 has soft shadow: {elev2}")
        assert_true("none" not in elev3, f"Elevation 3 has soft shadow: {elev3}")
        assert_true("none" not in elev4, f"Elevation 4 has soft shadow: {elev4}")

        elev_shot = os.path.join(ARTIFACT_DIR, "elevation_shadow_levels.png")
        page.locator("#sectionElevation").screenshot(path=elev_shot)
        assert_true(os.path.exists(elev_shot), "Elevation levels artifact screenshot captured")

        # ── 5. Verify Natural Hover & Active Press States ──
        log("Verifying Natural Hover & Press Animations (Section 10)...")
        icard = page.locator("#demoInteractiveCard1")
        icard.hover()
        page.wait_for_timeout(200)
        hover_bg = icard.evaluate("el => window.getComputedStyle(el).backgroundColor")
        assert_true("rgba(0, 0, 0, 0)" not in hover_bg and "transparent" not in hover_bg, f"Card preserves solid background on hover: {hover_bg}")

        btn_hover = os.path.join(ARTIFACT_DIR, "button_sizes_and_variants.png")
        page.locator("#sectionButtonSizes").screenshot(path=btn_hover)
        assert_true(os.path.exists(btn_hover), "Button sizes and variants artifact screenshot captured")

        # ── 6. Verify Form Controls Standardization ──
        log("Verifying Form Controls (Section 12)...")
        inp_std = page.locator("#inputStandardSample")
        inp_h = inp_std.evaluate("el => window.getComputedStyle(el).height")
        inp_r = inp_std.evaluate("el => window.getComputedStyle(el).borderRadius")
        assert_true(inp_h == "40px", f"Standard input height is 40px (computed: {inp_h})")
        assert_true(inp_r == "8px", f"Standard input radius is 8px (computed: {inp_r})")

        sel_std = page.locator("#selectSample")
        sel_h = sel_std.evaluate("el => window.getComputedStyle(el).height")
        sel_r = sel_std.evaluate("el => window.getComputedStyle(el).borderRadius")
        assert_true(sel_h == "40px", f"Standard select height is 40px (computed: {sel_h})")
        assert_true(sel_r == "8px", f"Standard select radius is 8px (computed: {sel_r})")

        # ── 7. Verify Data Table Interface ──
        log("Verifying Data Table Interface (Section 13)...")
        tbl_th = page.locator(".ngis-table th").first
        th_weight = tbl_th.evaluate("el => window.getComputedStyle(el).fontWeight")
        assert_true(int(th_weight) <= 500, f"Table header font-weight <= 500 (computed: {th_weight})")

        # ── 8. Verify Dark Theme Overrides ──
        log("Verifying Dark Mode Theme...")
        page.click("#themeToggleBtn")
        page.wait_for_timeout(300)
        dark_theme = page.evaluate("() => document.documentElement.getAttribute('data-theme')")
        assert_true(dark_theme == "dark", "Dark mode activated")
        dark_shot = os.path.join(ARTIFACT_DIR, "design_system_preview_dark.png")
        page.screenshot(path=dark_shot, full_page=True)
        assert_true(os.path.exists(dark_shot), "Dark mode preview screenshot captured")

        # Toggle back to light
        page.click("#themeToggleBtn")
        page.wait_for_timeout(200)

        page.close()

        # ── 9. Test Mobile Responsive Viewports (320px, 375px, 390px, 430px) ──
        for width in [320, 375, 390, 430]:
            log(f"Testing Mobile Viewport {width}px...")
            mob_page = browser.new_page(viewport={"width": width, "height": 812})
            mob_page.goto("http://127.0.0.1:3000/pages/shared/design-system-preview.html", wait_until="networkidle")

            # Check Mobile Hamburger Button & Touch Target
            hamb = mob_page.locator(".mobile-hamburger-btn")
            assert_true(hamb.is_visible(), f"Mobile hamburger button visible at {width}px")
            hamb_box = hamb.bounding_box()
            assert_true(hamb_box and hamb_box["width"] >= 44 and hamb_box["height"] >= 44, f"Mobile touch target >= 44x44px at {width}px (actual: {hamb_box['width'] if hamb_box else 0}x{hamb_box['height'] if hamb_box else 0}px)")

            # Check No Horizontal Overflow
            scroll_w = mob_page.evaluate("() => document.documentElement.scrollWidth")
            client_w = mob_page.evaluate("() => document.documentElement.clientWidth")
            assert_true(scroll_w <= client_w + 1, f"No accidental horizontal scroll at {width}px (scrollWidth={scroll_w}, clientWidth={client_w})")

            if width == 375:
                mob_shot = os.path.join(ARTIFACT_DIR, "design_system_preview_mobile_375.png")
                mob_page.screenshot(path=mob_shot, full_page=True)
                assert_true(os.path.exists(mob_shot), "Mobile 375px preview screenshot captured")

            mob_page.close()

        # ── 10. Test Key Portal Pages Across Desktop & Mobile ──
        portal_pages = [
            ("Admin Dashboard", "http://127.0.0.1:3000/pages/admin/admin.html"),
            ("Admin Classes", "http://127.0.0.1:3000/pages/admin/admin-classes.html"),
            ("Student Roadmap", "http://127.0.0.1:3000/pages/student/student-exams.html"),
            ("Teacher Attendance", "http://127.0.0.1:3000/pages/teacher/teacher-attendance.html"),
            ("Principal Reports", "http://127.0.0.1:3000/pages/principal/principal-reports.html")
        ]

        for name, url in portal_pages:
            log(f"Verifying {name} across viewports...")
            # Desktop 1440
            p_desk = browser.new_page(viewport={"width": 1440, "height": 900})
            p_desk.goto(url, wait_until="networkidle")
            # Verify no bold fonts
            heavy_fonts = p_desk.evaluate("""() => {
                const els = Array.from(document.querySelectorAll('h1, h2, h3, h4, th, .btn, .card-title, label'));
                return els.filter(el => {
                    const fw = parseInt(window.getComputedStyle(el).fontWeight, 10);
                    return fw > 500;
                }).length;
            }""")
            assert_true(heavy_fonts == 0, f"{name} complies with strict NO BOLD rule (found {heavy_fonts} bold elements)")
            p_desk.close()

            # Mobile 375
            p_mob = browser.new_page(viewport={"width": 375, "height": 812})
            p_mob.goto(url, wait_until="networkidle")
            # Verify hamburger menu exists on mobile
            hamb_mob = p_mob.locator('[data-action="toggle-sidebar"]').first
            assert_true(hamb_mob.is_visible(), f"{name} displays mobile navigation hamburger button")
            p_mob.close()

        browser.close()
        log("ALL TESTS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    run_tests()
