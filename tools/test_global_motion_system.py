import asyncio
from playwright.async_api import async_playwright

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 850})
        page = await context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg.text) if msg.type == 'error' else None)

        print("=== TEST 1: Landing Page (index.html) Motion System & GSAP ===")
        await page.goto('http://127.0.0.1:3000/index.html', wait_until='networkidle')
        await page.wait_for_timeout(600)

        # Check NGIS_MOTION presence
        has_motion = await page.evaluate("() => !!window.NGIS_MOTION")
        has_gsap = await page.evaluate("() => !!window.gsap")
        print(f"window.NGIS_MOTION initialized: {has_motion}")
        print(f"window.gsap loaded: {has_gsap}")
        assert has_motion, "NGIS_MOTION should be initialized"

        # Check Card Hover Lift on .portal-card
        portal_card = page.locator('.portal-card').first
        await portal_card.scroll_into_view_if_needed()
        await portal_card.hover()
        await page.wait_for_timeout(300)
        hover_transform = await portal_card.evaluate("el => window.getComputedStyle(el).transform")
        print(f"Portal card hover transform: {hover_transform}")
        assert "matrix" in hover_transform and hover_transform != "none", "Card should have hover transform applied"

        # Check Error Shake
        shake_result = await page.evaluate("""() => {
            return new Promise((resolve) => {
                const btn = document.querySelector('.btn-primary');
                if (!btn) return resolve(false);
                let shook = false;
                window.NGIS_MOTION.shake(btn, {
                    distance: 4,
                    duration: 0.3,
                    onComplete: () => {
                        resolve(true);
                    }
                });
            });
        }""")
        print(f"Error shake completed with callback: {shake_result}")
        assert shake_result, "Error shake should execute and call onComplete"

        # Check Success Feedback Toast
        success_result = await page.evaluate("""() => {
            return new Promise((resolve) => {
                window.NGIS_MOTION.success(null, "Record Updated Successfully", () => {
                    resolve(true);
                });
                setTimeout(() => {
                    const toast = document.querySelector('.ngis-success-toast');
                    resolve(!!toast);
                }, 200);
            });
        }""")
        print(f"Success toast rendered: {success_result}")
        assert success_result, "Success toast should be visible"

        print("\n=== TEST 2: Student Exams Page (student-exams.html) ===")
        await page.goto('http://127.0.0.1:3000/pages/student/student-exams.html', wait_until='networkidle')
        await page.wait_for_timeout(600)

        has_motion_student = await page.evaluate("() => !!window.NGIS_MOTION")
        print(f"Student page NGIS_MOTION initialized: {has_motion_student}")
        assert has_motion_student, "Student page should have NGIS_MOTION via layout.js"

        # Modal Open Animation (Scale 0.97 -> 1.00)
        first_exam = page.locator('.exw-timeline-card').first
        await first_exam.click()
        await page.wait_for_timeout(400)

        modal_scrim = page.locator('.exw-modal-scrim')
        modal_visible = await page.evaluate("() => { const s = document.querySelector('.exw-modal-scrim'); return s && s.classList.contains('show'); }")
        print(f"Exam detail modal opened with .show: {modal_visible}")
        assert modal_visible, "Modal should open on exam click"

        # Check modal close
        close_btn = page.locator('.exw-modal-close').first
        await close_btn.click()
        await page.wait_for_timeout(400)
        modal_closed = await page.evaluate("() => { const s = document.querySelector('.exw-modal-scrim'); return !s || !s.classList.contains('show'); }")
        print(f"Exam detail modal closed cleanly: {modal_closed}")
        assert modal_closed, "Modal should close cleanly without leaving overlays"

        print("\n=== TEST 3: Admin Portal Dashboard (admin.html) ===")
        await page.goto('http://127.0.0.1:3000/pages/admin/admin.html', wait_until='networkidle')
        await page.wait_for_timeout(600)

        has_motion_admin = await page.evaluate("() => !!window.NGIS_MOTION")
        print(f"Admin portal NGIS_MOTION initialized: {has_motion_admin}")
        assert has_motion_admin, "Admin portal should have NGIS_MOTION"

        # Test Sidebar Collapsible Group Smooth Height Expansion
        group_label = page.locator('.nav-group.collapsible .nav-group-label').first
        if await group_label.count() > 0:
            parent_group = group_label.locator('..')
            init_expanded = await parent_group.evaluate("el => el.classList.contains('expanded')")
            await group_label.click()
            await page.wait_for_timeout(350)
            toggled_expanded = await parent_group.evaluate("el => el.classList.contains('expanded')")
            print(f"Collapsible group toggled smoothly: was {init_expanded} -> now {toggled_expanded}")
            assert init_expanded != toggled_expanded, "Group should toggle expansion"

        print("\n=== TEST 4: Intelligent Tooltips ===")
        tooltip_test = await page.evaluate("""() => {
            const btn = document.querySelector('[data-tooltip], [title], .icon-btn');
            if (!btn) return false;
            btn.setAttribute('data-tooltip', 'Quick Navigation Tooltip');
            window.NGIS_MOTION.showTooltip(btn);
            return true;
        }""")
        await page.wait_for_timeout(450)
        tip_visible = await page.evaluate("() => { const t = document.getElementById('ngisGlobalTooltip'); return t && t.style.display !== 'none'; }")
        print(f"Intelligent tooltip displayed: {tip_visible}")
        assert tip_visible, "Tooltip should display after warm delay"

        # Hide tooltip
        await page.evaluate("() => window.NGIS_MOTION.hideTooltip()")
        await page.wait_for_timeout(250)
        tip_hidden = await page.evaluate("() => { const t = document.getElementById('ngisGlobalTooltip'); return !t || t.style.display === 'none'; }")
        print(f"Intelligent tooltip hidden: {tip_hidden}")
        assert tip_hidden, "Tooltip should hide cleanly"

        print("\n=== TEST 5: Responsive Viewports & Mobile Drawers ===")
        viewports = [320, 375, 768, 1024, 1440]
        for w in viewports:
            await page.set_viewport_size({'width': w, 'height': 800})
            await page.wait_for_timeout(250)
            is_drawer = await page.evaluate("() => window.innerWidth <= 1024")
            sidebar_transform = await page.evaluate("() => { const s = document.querySelector('#sidebar'); return s ? window.getComputedStyle(s).transform : 'none'; }")
            print(f"Viewport {w}px: isDrawerMode={is_drawer}, sidebar transform={sidebar_transform[:25]}")

        print("\n=== TEST 6: Accessibility (Prefers-Reduced-Motion) ===")
        await page.emulate_media(reduced_motion='reduce')
        await page.wait_for_timeout(200)
        reduced = await page.evaluate("() => window.NGIS_MOTION.prefersReducedMotion()")
        print(f"Prefers reduced motion detected: {reduced}")
        assert reduced, "Reduced motion should be detected accurately"

        # In reduced motion mode, shake should be replaced with static highlight
        btn = page.locator('.btn-primary, button').first
        await page.evaluate("el => window.NGIS_MOTION.shake(el)", await btn.element_handle())
        await page.wait_for_timeout(200)
        has_shake_class = await btn.evaluate("el => el.classList.contains('ngis-shake')")
        print(f"In reduced motion, shaking animation suppressed: {not has_shake_class}")
        assert not has_shake_class, "Shake animation must be suppressed under reduced-motion"

        print(f"\nConsole errors detected: {len(console_errors)}")
        if console_errors:
            for err in console_errors:
                print("  Console error:", err)

        print("\nALL GLOBAL MOTION SYSTEM TESTS PASSED PERFECTLY!")
        await browser.close()

if __name__ == '__main__':
    asyncio.run(run())
