import os
import shutil
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"


def run_tests():
    print("Starting Playwright E2E for NGIS Admin Dashboard Content Manager...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ── 1. Desktop Verification (admin-dashboard-content.html) ───────────
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        url = "http://127.0.0.1:3000/pages/admin/admin-dashboard-content.html"
        print(f"Navigating to {url} at 1440x900...")
        page.goto(url, wait_until="networkidle")
        time.sleep(1.5)

        title = page.title()
        print("Page title:", title)
        assert "Dashboard Content Manager" in title

        # Verify initial Hero preview
        pv_title = page.locator("#pvHeroTitle").inner_text()
        pv_greeting = page.locator("#pvHeroGreeting").inner_text()
        print(f"Initial Preview -> Title: '{pv_title}', Greeting: '{pv_greeting}'")
        assert "Welcome" in pv_title
        assert "Nrinphouneta" in pv_greeting

        # Capture initial desktop screenshot
        desktop_img = "scratch/admin_cms_desktop_1440.png"
        page.screenshot(path=desktop_img, full_page=True)
        print("Captured desktop screenshot:", desktop_img)

        # ── 2. Test Reactive Real-time Live Preview Editing ─────────────────
        print("Testing reactive live preview on title input...")
        title_input = page.locator("#cmsHeroTitle")
        title_input.fill("Welcome to New Gateway International School")
        time.sleep(0.4)

        updated_pv_title = page.locator("#pvHeroTitle").inner_text()
        print("Updated Preview Title:", updated_pv_title)
        assert updated_pv_title == "Welcome to New Gateway International School"

        # Insert token chip
        print("Clicking token chip + {school_name}...")
        page.locator(".cms-token-chip:has-text('{school_name}')").click()
        time.sleep(0.4)
        updated_pv_greeting = page.locator("#pvHeroGreeting").inner_text()
        print("Updated Greeting:", updated_pv_greeting)
        assert "New Gateway" in updated_pv_greeting

        reactive_img = "scratch/admin_cms_reactive_edit.png"
        page.screenshot(path=reactive_img)
        print("Captured reactive edit screenshot:", reactive_img)

        # ── 3. Test Banner Management Interaction ───────────────────────────
        print("Switching to Banners tab...")
        page.locator(".cms-tab-btn[data-tab='tabBanners']").click()
        time.sleep(0.3)

        # Verify banner list
        banner_items = page.locator("#cmsBannerList .cms-banner-item")
        b_count = banner_items.count()
        print(f"Found {b_count} configured banner slides.")
        assert b_count >= 1

        # Add new banner slide
        print("Adding a new promotional slide...")
        page.locator("#cmsBtnAddNewBanner").click()
        time.sleep(0.4)

        page.locator("#cmsBannerHeading").fill("Special Cambridge Innovation Exhibition")
        time.sleep(0.4)
        pv_banner_heading = page.locator("#pvPromoHeading").inner_text()
        print("Preview banner heading:", pv_banner_heading)
        assert "Cambridge Innovation" in pv_banner_heading

        banner_img = "scratch/admin_cms_banner_editor.png"
        page.screenshot(path=banner_img)
        print("Captured banner editor screenshot:", banner_img)

        # ── 4. Test 'Edit on Preview' (Visual Edit Mode) ────────────────────
        print("Testing 'Edit on Preview' visual mode...")
        btn_visual = page.locator("#cmsBtnVisualMode")
        btn_visual.click()
        time.sleep(0.3)
        assert page.locator("#cmsPreviewViewport").evaluate("el => el.classList.contains('cms-visual-mode')")

        # Click the hero block in preview to trigger tab switch back to Hero
        page.locator("#pvHero").click()
        time.sleep(0.3)
        assert page.locator(".cms-tab-btn[data-tab='tabHero']").evaluate("el => el.classList.contains('active')")
        print("Visual mode click successfully opened Hero editor tab!")

        # Turn off visual mode
        btn_visual.click()
        time.sleep(0.2)

        # ── 5. Test Save Draft & Public Isolation ───────────────────────────
        print("Saving draft changes...")
        page.locator("#cmsBtnSaveDraft").click()
        time.sleep(0.5)

        badge_text = page.locator("#cmsStatusBadge").inner_text()
        print("Status badge:", badge_text)
        assert "Draft" in badge_text

        # ── 6. Test Publish to Live ─────────────────────────────────────────
        print("Publishing changes to live...")
        page.on("dialog", lambda dialog: dialog.accept())
        page.locator("#cmsBtnPublish").click()
        time.sleep(1.0)

        pub_badge = page.locator("#cmsStatusBadge").inner_text()
        print("Published status badge:", pub_badge)
        assert "Published" in pub_badge

        # ── 7. Test Version History & Instant Rollback ──────────────────────
        print("Opening Version History & Rollback modal...")
        page.locator("#cmsBtnVersions").click()
        time.sleep(0.6)

        version_modal = page.locator("#cmsModalBackdrop")
        assert version_modal.is_visible()
        v_title = page.locator("#cmsModalTitle").inner_text()
        print("Version modal title:", v_title)
        assert "Version History" in v_title

        version_img = "scratch/admin_cms_version_modal.png"
        page.screenshot(path=version_img)
        print("Captured version modal screenshot:", version_img)

        # Close version modal
        page.locator("#cmsModalCloseBtn").click()
        time.sleep(0.4)

        # ── 8. Test Media Library Tab ───────────────────────────────────────
        print("Opening Media Library tab...")
        page.locator(".cms-tab-btn[data-tab='tabMedia']").click()
        time.sleep(0.5)

        media_cards = page.locator("#cmsMediaGrid .cms-media-card")
        media_count = media_cards.count()
        print(f"Found {media_count} media library items.")
        assert media_count >= 1

        media_img = "scratch/admin_cms_media_library.png"
        page.screenshot(path=media_img)
        print("Captured media library screenshot:", media_img)

        # ── 9. Typography Audit (NO BOLD FONTS) ──────────────────────────────
        print("Auditing font weights across elements (must not exceed 500)...")
        heavy_elements = page.evaluate("""() => {
            const all = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, button, a, div, th, td, label');
            let violations = [];
            for (let el of all) {
                const weight = window.getComputedStyle(el).fontWeight;
                if (parseInt(weight) > 500) {
                    violations.push({
                        tag: el.tagName,
                        text: el.innerText ? el.innerText.slice(0, 30) : '',
                        weight: weight
                    });
                }
            }
            return violations.slice(0, 10);
        }""")
        print(f"Typography audit: Found {len(heavy_elements)} elements with fontWeight > 500.")
        assert len(heavy_elements) == 0, f"Found bold elements: {heavy_elements}"

        # ── 10. Tablet Verification (768x1024) ──────────────────────────────
        page.set_viewport_size({"width": 768, "height": 1024})
        time.sleep(0.5)
        tablet_img = "scratch/admin_cms_tablet_768.png"
        page.screenshot(path=tablet_img, full_page=True)
        print("Captured tablet screenshot:", tablet_img)

        # ── 11. Mobile Verification (390x844) ───────────────────────────────
        page.set_viewport_size({"width": 390, "height": 844})
        time.sleep(0.5)

        hamburger = page.locator('button[data-action="toggle-sidebar"]').first
        assert hamburger.is_visible(), "Mandatory hamburger menu button MUST be visible on mobile!"
        print("Verified mandatory mobile hamburger menu button.")

        mobile_img = "scratch/admin_cms_mobile_390.png"
        page.screenshot(path=mobile_img, full_page=True)
        print("Captured mobile screenshot:", mobile_img)

        # Open mobile sidebar via hamburger
        hamburger.click()
        time.sleep(0.6)
        mobile_drawer_img = "scratch/admin_cms_mobile_drawer.png"
        page.screenshot(path=mobile_drawer_img)
        print("Captured mobile drawer screenshot:", mobile_drawer_img)

        # ── 12. Student Dashboard Live Verification ─────────────────────────
        page.set_viewport_size({"width": 1440, "height": 900})
        student_url = "http://127.0.0.1:3000/pages/student/student.html"
        print(f"Navigating to {student_url} to verify live dashboard...")
        page.goto(student_url, wait_until="networkidle")
        time.sleep(1.5)

        std_hero = page.locator(".hero-title").inner_text()
        print("Live Student Dashboard Hero Title:", std_hero)
        assert len(std_hero) > 0

        student_live_img = "scratch/student_dashboard_cms_live.png"
        page.screenshot(path=student_live_img, full_page=False)
        print("Captured live student dashboard screenshot:", student_live_img)

        # Copy all screenshots to artifact directory
        all_imgs = [desktop_img, reactive_img, banner_img, version_img, media_img, tablet_img, mobile_img, mobile_drawer_img, student_live_img]
        for img in all_imgs:
            fname = os.path.basename(img)
            dest = os.path.join(ARTIFACT_DIR, fname)
            shutil.copy2(img, dest)
            print(f"Copied {fname} to artifact dir.")

        browser.close()
        print("Playwright E2E for Dashboard CMS Completed Successfully!")


if __name__ == "__main__":
    run_tests()

