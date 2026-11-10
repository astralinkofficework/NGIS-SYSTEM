import os
import shutil
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"

def run_tests():
    print("Starting Playwright E2E for NGIS Admin IT Control Center...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # ── 1. Desktop Verification (admin-operations-control.html) ───────────
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        url = "http://127.0.0.1:3000/pages/admin/admin-operations-control.html"
        print(f"Navigating to {url} at 1440x900...")
        page.goto(url, wait_until="networkidle")
        time.sleep(1.5)

        # Verify title
        title = page.title()
        print("Page title:", title)
        assert "School Operations" in title or "Control Center" in title

        # Verify 5 KPIs
        kpi_op = page.locator("#kpiOpsModules").inner_text()
        kpi_inc = page.locator("#kpiOpsIncomplete").inner_text()
        kpi_miss = page.locator("#kpiOpsMissing").inner_text()
        kpi_err = page.locator("#kpiOpsErrors").inner_text()
        kpi_rev = page.locator("#kpiOpsReviews").inner_text()
        print(f"KPIs -> Operational: {kpi_op}, Incomplete: {kpi_inc}, Missing: {kpi_miss}, Errors: {kpi_err}, Reviews: {kpi_rev}")
        assert int(kpi_op) >= 1
        assert int(kpi_miss) >= 10

        # Verify 6 Monitoring Cards
        cards = page.locator("#opsMonitoringCardsContainer .ops-card")
        card_count = cards.count()
        print(f"Found {card_count} monitoring cards in 3x2 grid.")
        assert card_count == 6, f"Expected 6 monitoring cards, got {card_count}"

        # Capture Desktop Full Overview
        desktop_img = "scratch/admin_control_center_desktop_1440.png"
        page.screenshot(path=desktop_img, full_page=True)
        print("Captured desktop screenshot:", desktop_img)

        # ── 2. Click Attendance Card -> Opens Audit Modal ───────────────────
        print("Clicking Card 01 (Attendance) to inspect operational audit...")
        cards.nth(0).click()
        time.sleep(0.5)

        audit_modal = page.locator("#opsAuditModal")
        assert audit_modal.is_visible(), "Module audit modal should be visible"
        modal_title = page.locator("#opsAuditModalTitle").inner_text()
        print("Audit modal title:", modal_title)
        assert "Attendance" in modal_title

        audit_img = "scratch/admin_control_center_audit_modal.png"
        page.screenshot(path=audit_img)
        print("Captured audit modal screenshot:", audit_img)

        # Close audit modal
        page.locator("button:has-text('Close Audit')").click()
        time.sleep(0.5)

        # ── 3. Test Staff Reminder Modal from Issues Registry ───────────────
        print("Testing Reminder Modal from Issues Registry...")
        btn_remind = page.locator("#opsIssuesTableBody button:has-text('Remind Owner')").first
        btn_remind.click()
        time.sleep(0.5)

        rem_modal = page.locator("#opsReminderModal")
        assert rem_modal.is_visible(), "Reminder modal should be visible"
        rem_recip = page.locator("#opsModalRecipientDisplay").inner_text()
        print("Reminder recipient:", rem_recip)

        remind_img = "scratch/admin_control_center_reminder_modal.png"
        page.screenshot(path=remind_img)
        print("Captured reminder modal screenshot:", remind_img)

        # Close reminder modal
        page.locator("#opsReminderModal button:has-text('Cancel')").click()
        time.sleep(0.5)

        # ── 4. Verify Technical System Health & Pipeline ───────────────────
        health_cards = page.locator("#opsSystemHealthContainer > div > div")
        health_count = health_cards.count()
        print(f"Verified {health_count} technical system health probes.")
        assert health_count >= 4, f"Expected 4 health probes, got {health_count}"

        # ── 5. Typography Audit (NO BOLD FONTS) ──────────────────────────────
        print("Auditing font weights across elements...")
        heavy_elements = page.evaluate("""() => {
            const all = document.querySelectorAll('h1, h2, h3, h4, h5, h6, p, span, button, a, div, th, td');
            let violations = [];
            for (let el of all) {
                const weight = window.getComputedStyle(el).fontWeight;
                if (parseInt(weight) > 500) {
                    violations.push({
                        tag: el.tagName,
                        text: el.innerText.slice(0, 30),
                        weight: weight
                    });
                }
            }
            return violations.slice(0, 10);
        }""")
        print(f"Typography audit: Found {len(heavy_elements)} elements with fontWeight > 500.")
        assert len(heavy_elements) == 0, f"Found bold elements: {heavy_elements}"

        # ── 6. Tablet Verification (768x1024) ───────────────────────────────
        page.set_viewport_size({"width": 768, "height": 1024})
        time.sleep(0.5)
        tablet_img = "scratch/admin_control_center_tablet_768.png"
        page.screenshot(path=tablet_img, full_page=True)
        print("Captured tablet screenshot:", tablet_img)

        # ── 7. Mobile Verification (390x844) ────────────────────────────────
        page.set_viewport_size({"width": 390, "height": 844})
        time.sleep(0.5)
        
        hamburger = page.locator('button[data-action="toggle-sidebar"]').first
        assert hamburger.is_visible(), "Mandatory hamburger menu button MUST be visible on mobile!"
        print("Verified mandatory mobile hamburger menu button.")

        mobile_img = "scratch/admin_control_center_mobile_390.png"
        page.screenshot(path=mobile_img, full_page=True)
        print("Captured mobile screenshot:", mobile_img)

        # Open mobile sidebar via hamburger
        hamburger.click()
        time.sleep(0.6)
        mobile_drawer_img = "scratch/admin_control_center_mobile_drawer.png"
        page.screenshot(path=mobile_drawer_img)
        print("Captured mobile drawer open screenshot:", mobile_drawer_img)

        # ── 8. Verify Admin Main Dashboard Integration (admin.html) ─────────
        page.set_viewport_size({"width": 1440, "height": 900})
        admin_url = "http://127.0.0.1:3000/pages/admin/admin.html"
        print(f"Navigating to {admin_url} to verify integrated dashboard...")
        page.goto(admin_url, wait_until="networkidle")
        time.sleep(1.5)

        dash_ops = page.locator("#secOpsControl")
        assert dash_ops.is_visible(), "Operations Control Center MUST be integrated in admin.html!"
        print("Verified Operations Control Center section in admin.html!")

        admin_dash_img = "scratch/admin_dashboard_integrated_1440.png"
        page.screenshot(path=admin_dash_img, full_page=False)
        print("Captured integrated admin.html screenshot:", admin_dash_img)

        # Copy all screenshots to artifact directory
        for img in [desktop_img, audit_img, remind_img, tablet_img, mobile_img, mobile_drawer_img, admin_dash_img]:
            fname = os.path.basename(img)
            dest = os.path.join(ARTIFACT_DIR, fname)
            shutil.copy2(img, dest)
            print(f"Copied {fname} to artifact dir.")

        browser.close()
        print("Playwright E2E for Admin IT Control Center Completed Successfully!")

if __name__ == "__main__":
    run_tests()

