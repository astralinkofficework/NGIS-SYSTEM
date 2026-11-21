import asyncio
import os
from playwright.async_api import async_playwright

VIEWPORTS = [
    {"name": "mobile_320", "width": 320, "height": 568},
    {"name": "mobile_375", "width": 375, "height": 667},
    {"name": "mobile_390", "width": 390, "height": 844},
    {"name": "mobile_430", "width": 430, "height": 932},
    {"name": "tablet_768", "width": 768, "height": 1024},
    {"name": "tablet_1024", "width": 1024, "height": 768},
    {"name": "desktop_1440", "width": 1440, "height": 900},
    {"name": "desktop_1920", "width": 1920, "height": 1080},
]

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\f0e0db56-cd04-4f51-a7f8-40ba21b43536"

async def run_tests():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # 1. Desktop Test & Interaction Verification (1440x900)
        context = await browser.new_context(viewport={"width": 1440, "height": 900})
        page = await context.new_page()

        print("[Test] Loading http://127.0.0.1:3000/pages/shared/ux-demo.html...")
        await page.goto("http://127.0.0.1:3000/pages/shared/ux-demo.html", wait_until="networkidle")
        await page.wait_for_selector("body.ngis-layout-ready", timeout=5000)

        # Capture Desktop Full Overview
        desktop_shot = os.path.join(ARTIFACT_DIR, "ux_demo_desktop_1440.png")
        await page.screenshot(path=desktop_shot, full_page=True)
        print(f"[Screenshot] Desktop saved: {desktop_shot}")

        # 2. Test Intelligent Dialog: Delete Student
        print("[Test] Triggering Delete Student dialog...")
        await page.evaluate("document.getElementById('btnDelStudent').click()")
        await page.wait_for_selector(".ngis-dialog-backdrop.is-visible", timeout=3000)

        # Check Dialog Contents
        title = await page.text_content("#ngisDialogTitle")
        desc = await page.text_content("#ngisDialogDesc")
        badge = await page.text_content(".ngis-dialog-badge")
        print(f"  Dialog Title: {title}")
        print(f"  Dialog Badge: {badge}")
        assert "Delete Alice Hok?" in title, f"Unexpected title: {title}"
        assert "Cannot be undone" in badge, f"Unexpected badge: {badge}"

        # Test Tab key cycling
        await page.keyboard.press("Tab")
        active_tag = await page.evaluate("document.activeElement.tagName")
        print(f"  Focused element after Tab: {active_tag}")

        # Test Escape to close
        print("[Test] Testing Escape key dismissal...")
        await page.keyboard.press("Escape")
        await page.wait_for_timeout(300)
        is_open = await page.is_visible("#ngisUniversalDialogBackdrop")
        assert not is_open, "Dialog failed to close on Escape!"
        print("  Escape successfully dismissed dialog.")

        # Reopen and confirm
        print("[Test] Reopening dialog and confirming action...")
        await page.evaluate("document.getElementById('btnDelStudent').click()")
        await page.wait_for_selector(".ngis-dialog-backdrop.is-visible", timeout=3000)
        await page.evaluate("document.querySelector('.ngis-dialog-confirm-btn').click()")
        await page.wait_for_timeout(300)

        # Verify animated success toast
        await page.wait_for_selector(".ngis-success-toast-item", timeout=3000)
        toast_text = await page.text_content(".ngis-success-text")
        print(f"  Success Toast: {toast_text}")
        assert "Alice Hok was archived successfully" in toast_text

        # 3. Test Tooltip with Warm Grouping
        print("[Test] Testing semantic tooltips...")
        download_btn = page.locator('[data-tooltip="Download original file"]')
        await download_btn.hover()
        await page.wait_for_timeout(450)
        tip_text = await page.text_content(".ngis-universal-tooltip")
        print(f"  Tooltip Text: {tip_text}")
        assert "Download original file" in tip_text

        # Move to adjacent button with shortcut key
        search_btn = page.locator('[data-key-binding="ctrl+k"]')
        await search_btn.hover()
        await page.wait_for_timeout(80) # warm skip
        tip_text_2 = await page.text_content(".ngis-universal-tooltip")
        print(f"  Warm Tooltip Text: {tip_text_2}")
        assert "search" in tip_text_2.lower()

        # 4. Test Inline Validation
        print("[Test] Testing inline field validation...")
        await page.evaluate("document.getElementById('btnTestValidate').click()")
        await page.wait_for_selector(".ngis-inline-error", timeout=2000)
        err_msg = await page.text_content(".ngis-inline-error")
        print(f"  Validation Error: {err_msg}")
        assert "valid email address" in err_msg

        # 5. Mobile Bottom Sheet Verification (375x667)
        await context.close()
        mobile_ctx = await browser.new_context(viewport={"width": 375, "height": 667})
        mobile_page = await mobile_ctx.new_page()
        await mobile_page.goto("http://127.0.0.1:3000/pages/shared/ux-demo.html", wait_until="networkidle")
        await mobile_page.wait_for_selector("body.ngis-layout-ready", timeout=5000)

        # Trigger dialog on mobile
        await mobile_page.evaluate("document.getElementById('btnDelAssignment').click()")
        await mobile_page.wait_for_selector(".ngis-dialog-backdrop.is-visible", timeout=3000)
        await mobile_page.wait_for_timeout(300)

        # Capture Mobile Bottom Sheet Screenshot
        mobile_dialog_shot = os.path.join(ARTIFACT_DIR, "ux_dialog_mobile_375.png")
        await mobile_page.screenshot(path=mobile_dialog_shot)
        print(f"[Screenshot] Mobile Dialog Bottom Sheet saved: {mobile_dialog_shot}")

        # Check mobile dialog computed styles (bottom sheet alignment)
        card_styles = await mobile_page.evaluate("""() => {
            const card = document.querySelector('.ngis-dialog-card');
            const style = window.getComputedStyle(card);
            return {
                borderRadius: style.borderRadius,
                borderBottomLeftRadius: style.borderBottomLeftRadius,
                borderBottomRightRadius: style.borderBottomRightRadius,
                position: style.position,
                width: style.width
            };
        }""")
        print(f"  Mobile Dialog Styles: {card_styles}")

        # Dismiss mobile dialog
        await mobile_page.evaluate("document.querySelector('.ngis-dialog-cancel-btn').click()")
        await mobile_page.wait_for_timeout(300)

        # 6. Test Notifications View on Student Portal
        student_notif_page = await mobile_ctx.new_page()
        await student_notif_page.goto("http://127.0.0.1:3000/pages/student/student-notifications.html", wait_until="networkidle")
        await student_notif_page.wait_for_selector("body.ngis-layout-ready", timeout=5000)
        await student_notif_page.wait_for_timeout(300)

        # Capture Student Notifications Mobile Screenshot
        student_notif_shot = os.path.join(ARTIFACT_DIR, "student_notifications_mobile_375.png")
        await student_notif_page.screenshot(path=student_notif_shot, full_page=True)
        print(f"[Screenshot] Student Notifications Mobile saved: {student_notif_shot}")

        # Test Mark all as read
        await student_notif_page.evaluate("document.getElementById('markAllReadBtn').click()")
        await student_notif_page.wait_for_timeout(300)
        badge_text = await student_notif_page.text_content("#unreadBadge")
        print(f"  Student Unread Badge after Mark All: {badge_text}")
        assert "0 unread" in badge_text

        # 7. Multi-Viewport Responsive Matrix Sweep
        print("\n[Test] Running Responsive Viewport Matrix Sweep across 8 viewports...")
        for vp in VIEWPORTS:
            ctx = await browser.new_context(viewport={"width": vp["width"], "height": vp["height"]})
            p_vp = await ctx.new_page()
            await p_vp.goto("http://127.0.0.1:3000/pages/shared/ux-demo.html", wait_until="networkidle")
            await p_vp.wait_for_selector("body.ngis-layout-ready", timeout=5000)
            
            # Check for horizontal overflow
            scroll_width = await p_vp.evaluate("document.documentElement.scrollWidth")
            client_width = await p_vp.evaluate("document.documentElement.clientWidth")
            overflow = scroll_width > client_width
            
            print(f"  Viewport {vp['name']} ({vp['width']}x{vp['height']}): scrollWidth={scroll_width}, clientWidth={client_width}, overflow={overflow}")
            assert not overflow, f"Horizontal overflow detected on viewport {vp['name']}!"
            await ctx.close()

        await mobile_ctx.close()
        await browser.close()
        print("\n[SUCCESS] ALL UX TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    asyncio.run(run_tests())
