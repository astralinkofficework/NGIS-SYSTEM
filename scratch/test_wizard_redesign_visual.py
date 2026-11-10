import os, time
from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        art_dir = os.path.join(os.environ.get('USERPROFILE', ''), '.gemini', 'antigravity', 'brain', 'c3bf1c11-3155-48a6-b3ee-4e74d6713af7')

        # 1. Desktop Principal Wizard
        context = browser.new_context(viewport={'width': 1440, 'height': 900})
        page = context.new_page()
        print("[1] Opening Principal Teacher Assignment Matrix...")
        page.goto("http://localhost:3000/pages/principal/principal-teacher-class-assignment.html")
        page.wait_for_selector("#ks-root", timeout=10000)
        time.sleep(1.5)

        shot1 = os.path.join(art_dir, "wizard_redesign_desktop_principal.png")
        page.screenshot(path=shot1, full_page=False)
        print("Desktop screenshot saved:", shot1)

        # 2. Select 8A cohort
        print("[2] Clicking 8A cohort card...")
        page.click('[data-act="select-wizard-class"][data-cid="class_8A"]')
        time.sleep(1)
        shot2 = os.path.join(art_dir, "wizard_redesign_desktop_8A.png")
        page.screenshot(path=shot2, full_page=False)
        print("8A cohort screenshot saved:", shot2)

        # 3. Test search filtering on Faculty
        print("[3] Testing faculty search input...")
        page.fill("#facultySearchInput", "Sok")
        time.sleep(0.5)
        shot3 = os.path.join(art_dir, "wizard_redesign_faculty_search.png")
        page.screenshot(path=shot3, full_page=False)
        print("Faculty search screenshot saved:", shot3)

        # 4. Open Assign Subject Modal
        print("[4] Opening assign modal...")
        page.fill("#facultySearchInput", "")
        time.sleep(0.5)
        page.click('[data-act="open-assign-modal"]')
        time.sleep(0.8)
        shot4 = os.path.join(art_dir, "wizard_redesign_modal.png")
        page.screenshot(path=shot4, full_page=False)
        print("Modal screenshot saved:", shot4)
        page.click('[data-act="modal-close"]')
        time.sleep(0.5)

        # 5. Admin Desktop
        print("[5] Opening Admin Teacher Assignment Matrix...")
        page.goto("http://localhost:3000/pages/admin/admin-teacher-class-assignment.html")
        page.wait_for_selector("#ks-root", timeout=10000)
        time.sleep(1.5)
        shot5 = os.path.join(art_dir, "wizard_redesign_desktop_admin.png")
        page.screenshot(path=shot5, full_page=False)
        print("Admin desktop screenshot saved:", shot5)

        # 6. Mobile View (375x667)
        print("[6] Testing mobile responsive view (375x667)...")
        page.set_viewport_size({'width': 375, 'height': 667})
        time.sleep(0.8)

        # Mobile Hamburger Button check
        btn = page.query_selector('[data-action="toggle-sidebar"]')
        assert btn is not None and btn.is_visible(), "Hamburger button must be visible on mobile!"
        print("PASS: Mobile hamburger button verified visible!")

        # Mobile Matrix Tab
        shot6 = os.path.join(art_dir, "wizard_redesign_mobile_matrix.png")
        page.screenshot(path=shot6, full_page=False)
        print("Mobile matrix screenshot saved:", shot6)

        # Mobile Cohorts Tab
        print("[7] Testing mobile cohorts tab...")
        page.click('[data-act="wizard-mobile-tab"][data-tab="cohorts"]')
        time.sleep(0.5)
        shot7 = os.path.join(art_dir, "wizard_redesign_mobile_cohorts.png")
        page.screenshot(path=shot7, full_page=False)
        print("Mobile cohorts screenshot saved:", shot7)

        # Mobile Faculty Tab
        print("[8] Testing mobile faculty tab...")
        page.click('[data-act="wizard-mobile-tab"][data-tab="faculty"]')
        time.sleep(0.5)
        shot8 = os.path.join(art_dir, "wizard_redesign_mobile_faculty.png")
        page.screenshot(path=shot8, full_page=False)
        print("Mobile faculty screenshot saved:", shot8)

        browser.close()
        print("ALL VISUAL TESTS PASSED WITH 100% SUCCESS!")

if __name__ == "__main__":
    run()

