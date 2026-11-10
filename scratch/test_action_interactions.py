from playwright.sync_api import sync_playwright

def test_interactions():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        errors = []
        page.on("console", lambda msg: errors.append(f"[{msg.type}] {msg.text}") if msg.type == "error" else None)
        page.on("pageerror", lambda err: errors.append(f"[pageerror] {err}"))

        # 1. Admin Grade Release
        print("\n--- Testing Admin Grade Release Interactions ---")
        page.goto("http://127.0.0.1:3000/pages/admin/admin-grade-release.html")
        page.wait_for_timeout(500)
        auth_btns = page.locator("button.btn-authorize")
        if auth_btns.count() > 0:
            auth_btns.first.click()
            print("Clicked first authorize button successfully.")
        page.wait_for_timeout(300)

        # 2. Principal Reports
        print("\n--- Testing Principal Reports Interactions ---")
        page.goto("http://127.0.0.1:3000/pages/principal/principal-reports.html")
        page.wait_for_timeout(500)
        pr_auth = page.locator("button.btn-authorize")
        if pr_auth.count() > 0:
            pr_auth.first.click()
            print("Clicked principal reports authorize button successfully.")
        page.wait_for_timeout(300)

        # 3. Principal Attendance
        print("\n--- Testing Principal Attendance Modals ---")
        page.goto("http://127.0.0.1:3000/pages/principal/principal-attendance.html")
        page.wait_for_timeout(500)
        # Click audit/correction button
        edit_btn = page.locator("button[onclick*='openCorrectionModal']").first
        if edit_btn.count() > 0:
            edit_btn.click()
            page.wait_for_timeout(300)
            modal = page.locator("#correctionModal")
            print("Correction modal open status:", modal.is_visible())
            # close modal
            page.keyboard.press("Escape")

        # 4. Principal Timetables
        print("\n--- Testing Principal Timetables Toggle ---")
        page.goto("http://127.0.0.1:3000/pages/principal/principal-timetables.html")
        page.wait_for_timeout(500)
        toggle_btn = page.locator("button[onclick*='toggleCohortSchedule']").first
        if toggle_btn.count() > 0:
            toggle_btn.click()
            page.wait_for_timeout(500)
            print("Toggled cohort schedule successfully.")

        # 5. Principal Services
        print("\n--- Testing Principal Services Actions ---")
        page.goto("http://127.0.0.1:3000/pages/principal/principal-services.html")
        page.wait_for_timeout(500)
        svc_btn = page.locator("button.action-icon-btn.primary").first
        if svc_btn.count() > 0:
            svc_btn.click()
            page.wait_for_timeout(300)
            print("Clicked services action successfully.")

        print(f"\nTotal Console / Page Errors Encountered: {len(errors)}")
        if errors:
            for err in errors:
                print(f"  ERR: {err}")
        else:
            print("SUCCESS: 0 errors during interaction testing!")

        browser.close()

if __name__ == "__main__":
    test_interactions()

