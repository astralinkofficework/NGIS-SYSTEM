import os
import shutil
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\oudom\.gemini\antigravity\brain\c3bf1c11-3155-48a6-b3ee-4e74d6713af7"

def run_tests():
    print("Starting Playwright E2E Verification for Admin Timetable Oversight...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        # ── 1. Desktop Verification (1440x900) ──────────────────────────────
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        url = "http://127.0.0.1:3000/pages/admin/admin-timetable-management.html"
        print(f"Navigating to {url} at 1440x900...")
        page.goto(url, wait_until="networkidle")
        time.sleep(1)

        # Verify page title
        title = page.title()
        print("Page title:", title)
        assert "Timetable Management" in title or "Timetable" in title

        # Verify 6 stages rendered
        stage_cards = page.locator("#workflowStagesContainer > div.cursor-pointer")
        stage_count = stage_cards.count()
        print(f"Found {stage_count} workflow stage cards.")
        assert stage_count == 6, f"Expected 6 stages, got {stage_count}"

        # Verify 4 KPI cards
        kpi_pct = page.locator("#kpiProgressPct").inner_text()
        kpi_comp = page.locator("#kpiCompletedTasks").inner_text()
        kpi_out = page.locator("#kpiOutstandingTasks").inner_text()
        print(f"KPIs -> Progress: {kpi_pct}, Completed: {kpi_comp}, Outstanding: {kpi_out}")

        # Capture Desktop Full Overview
        desktop_img = "scratch/admin_oversight_desktop_1440.png"
        page.screenshot(path=desktop_img, full_page=True)
        print("Captured desktop screenshot:", desktop_img)

        # ── 2. Click Stage Drawer (Step 04) ─────────────────────────────────
        print("Clicking Step 04 (Timetable Scheduling)...")
        stage_cards.nth(3).click()
        time.sleep(0.5)
        
        drawer = page.locator("#stageDrawer")
        assert drawer.is_visible(), "Stage drawer should be visible"
        drawer_img = "scratch/admin_oversight_stage_drawer.png"
        page.screenshot(path=drawer_img)
        print("Captured stage drawer screenshot:", drawer_img)

        # Close drawer
        page.locator("button:has-text('Close Panel')").click()
        time.sleep(0.5)

        # ── 3. Send Reminder Modal Test ─────────────────────────────────────
        print("Testing Reminder Modal on Class 7A...")
        btn_remind = page.locator("#outstandingTasksBody button:has-text('Send Reminder')").first
        btn_remind.click()
        time.sleep(0.5)

        modal = page.locator("#reminderModal")
        assert modal.is_visible(), "Reminder modal should be visible"
        
        modal_task = page.locator("#modalTaskDisplay").inner_text()
        modal_recip = page.locator("#modalRecipientDisplay").inner_text()
        print(f"Reminder Modal -> Task: {modal_task}, Recipient: {modal_recip}")

        modal_img = "scratch/admin_oversight_reminder_modal.png"
        page.screenshot(path=modal_img)
        print("Captured reminder modal screenshot:", modal_img)

        # Click Send in-app reminder
        print("Submitting reminder...")
        page.locator("#btnSubmitReminder").click()
        time.sleep(1)
        # Ensure modal is closed before moving to subsequent tests
        if page.locator("#reminderModal").is_visible():
            page.locator("#reminderModal button:has-text('Cancel')").click()
            time.sleep(0.5)

        # ── 4. Timetable Preview (Read-Only Grid) ───────────────────────────
        print("Verifying Timetable Preview Read-Only Grid...")
        page.locator("#sectionTimetablePreview").scroll_into_view_if_needed()
        
        # Switch to Class 7B to view complete placed timetable
        print("Switching preview to Class 7B...")
        page.select_option("#previewClassSelect", "class_7B")
        page.wait_for_selector("#timetableGridPreview table", state="visible", timeout=10000)
        time.sleep(1)

        preview_img = "scratch/admin_oversight_preview_grid.png"
        page.screenshot(path=preview_img)
        print("Captured read-only preview grid screenshot for Class 7B:", preview_img)

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
        if heavy_elements:
            print("Sample heavy elements (if any):", heavy_elements[:3])
        assert len(heavy_elements) == 0, f"Found bold elements violating AGENTS.md rule: {heavy_elements}"

        # ── 6. Tablet Verification (768x1024) ───────────────────────────────
        page.set_viewport_size({"width": 768, "height": 1024})
        time.sleep(0.5)
        tablet_img = "scratch/admin_oversight_tablet_768.png"
        page.screenshot(path=tablet_img, full_page=True)
        print("Captured tablet screenshot:", tablet_img)

        # ── 7. Mobile Verification (390x844) ────────────────────────────────
        page.set_viewport_size({"width": 390, "height": 844})
        time.sleep(0.5)
        
        # Check mandatory hamburger menu button
        hamburger = page.locator('button[data-action="toggle-sidebar"]').first
        assert hamburger.is_visible(), "Mandatory hamburger menu button MUST be visible on mobile!"
        print("Verified mandatory mobile hamburger menu button.")

        mobile_img = "scratch/admin_oversight_mobile_390.png"
        page.screenshot(path=mobile_img, full_page=True)
        print("Captured mobile screenshot:", mobile_img)

        # Open mobile sidebar via hamburger
        hamburger.click()
        time.sleep(0.6)
        mobile_drawer_img = "scratch/admin_oversight_mobile_drawer.png"
        page.screenshot(path=mobile_drawer_img)
        print("Captured mobile drawer open screenshot:", mobile_drawer_img)

        # Copy all screenshots to artifact directory
        for img in [desktop_img, drawer_img, modal_img, preview_img, tablet_img, mobile_img, mobile_drawer_img]:
            fname = os.path.basename(img)
            dest = os.path.join(ARTIFACT_DIR, fname)
            shutil.copy2(img, dest)
            print(f"Copied {fname} to artifact dir.")

        browser.close()
        print("Playwright E2E Verification Completed Successfully!")

if __name__ == "__main__":
    run_tests()
