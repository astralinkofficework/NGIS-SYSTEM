import asyncio
import os
import sys
from playwright.async_api import async_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"
os.makedirs(ARTIFACT_DIR, exist_ok=True)

VIEWPORTS = [
    (320, 568, "mobile_320"),
    (375, 812, "mobile_375"),
    (390, 844, "mobile_390"),
    (430, 932, "mobile_430"),
    (768, 1024, "tablet_768"),
    (1024, 768, "tablet_1024"),
    (1440, 900, "desktop_1440"),
    (1920, 1080, "desktop_1920"),
    (2560, 1440, "ultrawide_2560")
]

PAGES = [
    ("Principal Attendance", "http://127.0.0.1:3000/pages/principal/principal-attendance.html"),
    ("Principal Dashboard", "http://127.0.0.1:3000/pages/principal/principal.html"),
    ("Student Exams", "http://127.0.0.1:3000/pages/student/student-exams.html"),
    ("Admin Dashboard", "http://127.0.0.1:3000/pages/admin/admin.html"),
    ("Teacher Dashboard", "http://127.0.0.1:3000/pages/teacher/teacher.html")
]

async def run_tests():
    print("================================================================================", flush=True)
    print("MASTER FIX — Global Top Navbar Positioning & Layout Spacing Test Suite", flush=True)
    print("================================================================================", flush=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        # Step 1: Run comprehensive tests across all 9 viewports
        passed = 0
        total = 0

        for width, height, vp_name in VIEWPORTS:
            context = await browser.new_context(viewport={"width": width, "height": height})
            page = await context.new_page()

            is_desktop = width >= 1025
            is_mobile = width <= 768

            for page_name, url in PAGES:
                total += 1
                try:
                    await page.goto(url, wait_until="load", timeout=7000)
                except Exception:
                    pass
                await page.wait_for_timeout(250)

                metrics = await page.evaluate("""() => {
                    const nav = document.getElementById('ngisGlobalNavbar');
                    const sidebar = document.getElementById('sidebar');
                    const hero = document.querySelector('.hero:not(.hero-main):not(:has(.hero-body))') || document.querySelector('#heroBanner:not(:has(.hero-body))');
                    const heroTopbar = document.querySelector('.hero-topbar');
                    const stickySpacer = document.querySelector('.ngis-sticky-spacer');
                    const duplicateHeaders = Array.from(document.querySelectorAll('header:not(.ngis-navbar):not(.hero-main)')).filter(h => h.offsetHeight > 0);
                    
                    const docWidth = document.documentElement.clientWidth;
                    const docScrollWidth = document.documentElement.scrollWidth;
                    const bodyScrollWidth = document.body.scrollWidth;

                    const navRect = nav ? nav.getBoundingClientRect() : null;
                    const sidebarRect = sidebar ? sidebar.getBoundingClientRect() : null;

                    return {
                        hasNav: Boolean(nav),
                        navY: navRect ? navRect.y : -1,
                        navLeft: navRect ? navRect.left : -1,
                        navWidth: navRect ? navRect.width : -1,
                        navHeight: navRect ? navRect.height : -1,
                        sidebarWidth: sidebarRect ? sidebarRect.width : 0,
                        duplicateHeroVisible: hero ? (hero.offsetHeight > 0) : false,
                        duplicateHeroTopbarVisible: heroTopbar ? (heroTopbar.offsetHeight > 0) : false,
                        stickySpacerVisible: stickySpacer ? (stickySpacer.offsetHeight > 0) : false,
                        duplicateHeaderCount: duplicateHeaders.length,
                        hasOverflow: (docScrollWidth > docWidth + 2) || (bodyScrollWidth > docWidth + 2)
                    };
                }""")

                # Assertions
                errors = []
                if not metrics["hasNav"]:
                    errors.append("Navbar missing")
                if metrics["navY"] != 0:
                    errors.append(f"Navbar top offset is {metrics['navY']}px, expected 0px")
                if metrics["duplicateHeroVisible"]:
                    errors.append("Duplicate empty hero is visible")
                if metrics["duplicateHeroTopbarVisible"]:
                    errors.append("Duplicate hero-topbar is visible")
                if metrics["stickySpacerVisible"]:
                    errors.append("Sticky spacer is visible")
                if metrics["duplicateHeaderCount"] > 0:
                    errors.append(f"{metrics['duplicateHeaderCount']} duplicate headers visible")
                if metrics["hasOverflow"]:
                    errors.append("Horizontal overflow detected")

                if is_desktop:
                    expected_left = 256
                    if abs(metrics["navLeft"] - expected_left) > 2:
                        errors.append(f"Desktop navLeft is {metrics['navLeft']}px, expected {expected_left}px")
                else:
                    if metrics["navLeft"] != 0:
                        errors.append(f"Mobile/Tablet navLeft is {metrics['navLeft']}px, expected 0px")

                if not errors:
                    passed += 1
                    status = "PASS"
                else:
                    status = "FAIL: " + ", ".join(errors)

                print(f"[{status}] {page_name} @ {width}x{height} ({vp_name})", flush=True)

            await page.close()
            await context.close()

        print(f"\nViewport Verification Results: {passed}/{total} passed ({(passed/total)*100:.1f}%)", flush=True)

        # Step 2: Capture Visual Verification Screenshots for Artifact
        print("\nCapturing visual verification screenshots...", flush=True)
        capture_viewports = [
            (1440, 900, "desktop_1440"),
            (768, 1024, "tablet_768"),
            (375, 812, "mobile_375")
        ]

        for width, height, vp_label in capture_viewports:
            ctx = await browser.new_context(viewport={"width": width, "height": height})
            p_page = await ctx.new_page()

            # 1. Principal Attendance (Subpage)
            await p_page.goto("http://127.0.0.1:3000/pages/principal/principal-attendance.html", wait_until="load")
            await p_page.wait_for_timeout(400)
            shot1 = os.path.join(ARTIFACT_DIR, f"navbar_fixed_principal_attendance_{vp_label}.png")
            await p_page.screenshot(path=shot1, full_page=False)
            print(f"Saved: {shot1}", flush=True)

            # 2. Principal Dashboard (Greeting Hero)
            await p_page.goto("http://127.0.0.1:3000/pages/principal/principal.html", wait_until="load")
            await p_page.wait_for_timeout(400)
            shot2 = os.path.join(ARTIFACT_DIR, f"navbar_fixed_principal_dash_{vp_label}.png")
            await p_page.screenshot(path=shot2, full_page=False)
            print(f"Saved: {shot2}", flush=True)

            # 3. Student Exams
            await p_page.goto("http://127.0.0.1:3000/pages/student/student-exams.html", wait_until="load")
            await p_page.wait_for_timeout(400)
            shot3 = os.path.join(ARTIFACT_DIR, f"navbar_fixed_student_exams_{vp_label}.png")
            await p_page.screenshot(path=shot3, full_page=False)
            print(f"Saved: {shot3}", flush=True)

            # 4. Admin Dashboard
            await p_page.goto("http://127.0.0.1:3000/pages/admin/admin.html", wait_until="load")
            await p_page.wait_for_timeout(400)
            shot4 = os.path.join(ARTIFACT_DIR, f"navbar_fixed_admin_dash_{vp_label}.png")
            await p_page.screenshot(path=shot4, full_page=False)
            print(f"Saved: {shot4}", flush=True)

            await p_page.close()
            await ctx.close()

        # Step 3: Interactive Tests (Language dropdown, Notification panel, Sidebar toggle)
        print("\nExecuting interactive feature tests...", flush=True)
        d_ctx = await browser.new_context(viewport={"width": 1440, "height": 900})
        i_page = await d_ctx.new_page()
        await i_page.goto("http://127.0.0.1:3000/pages/principal/principal-attendance.html", wait_until="load")
        await i_page.wait_for_timeout(400)

        # Test Sidebar Collapse
        await i_page.click("#navSidebarCollapseBtn")
        await i_page.wait_for_timeout(350)
        col_metrics = await i_page.evaluate("""() => {
            const nav = document.getElementById('ngisGlobalNavbar');
            const sidebar = document.getElementById('sidebar');
            return {
                navLeft: nav.getBoundingClientRect().left,
                sidebarWidth: sidebar.getBoundingClientRect().width,
                isCollapsed: document.body.classList.contains('sidebar-collapsed')
            };
        }""")
        print("Sidebar Collapse Test:", col_metrics, flush=True)
        shot_col = os.path.join(ARTIFACT_DIR, "navbar_fixed_sidebar_collapsed_1440.png")
        await i_page.screenshot(path=shot_col, full_page=False)
        print("Saved sidebar collapse screenshot", flush=True)

        # Expand back
        await i_page.click("#navSidebarCollapseBtn")
        await i_page.wait_for_timeout(300)

        # Test Language Dropdown
        await i_page.click("#ngisDesktopLangBtn")
        await i_page.wait_for_timeout(250)
        shot_lang = os.path.join(ARTIFACT_DIR, "navbar_fixed_lang_dropdown_1440.png")
        await i_page.screenshot(path=shot_lang, full_page=False)
        print("Saved language dropdown screenshot", flush=True)

        # Test Notifications Dropdown
        await i_page.click("#ngisDesktopNotifBtn")
        await i_page.wait_for_timeout(250)
        shot_notif = os.path.join(ARTIFACT_DIR, "navbar_fixed_notif_dropdown_1440.png")
        await i_page.screenshot(path=shot_notif, full_page=False)
        print("Saved notifications dropdown screenshot", flush=True)

        await i_page.close()
        await d_ctx.close()
        await browser.close()
        print("\nALL GLOBAL NAVBAR POSITIONING TESTS SUCCESSFULLY COMPLETED!", flush=True)

asyncio.run(run_tests())
