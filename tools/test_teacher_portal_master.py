import sys
import time
from playwright.sync_api import sync_playwright

def run_teacher_portal_master_audit():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        desktop_page = browser.new_page(viewport={"width": 1280, "height": 900})
        mobile_page = browser.new_page(viewport={"width": 375, "height": 812})

        results = {}

        # -------------------------------------------------------------
        # TEST 1: Teacher Sidebar & Navigation Structure
        # -------------------------------------------------------------
        print("\n--- TEST 1: Sidebar & Navigation Structure ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher.html")
        desktop_page.wait_for_load_state("networkidle")

        sidebar_html = desktop_page.locator("#appSidebar, .sidebar").first.inner_html()
        assert "Daily Attendance" in sidebar_html or "Attendance" in sidebar_html, "Missing Attendance in sidebar"
        assert "Student Roster" in sidebar_html or "Students" in sidebar_html, "Missing Student Roster in sidebar"
        assert "Assignments" in sidebar_html or "Submissions" in sidebar_html, "Missing Submissions in sidebar"
        assert "Academic Reports" in sidebar_html, "Missing Academic Reports in sidebar"
        assert "Learning Materials" in sidebar_html, "Missing Learning Materials in sidebar"
        assert "Digital Faculty ID" not in sidebar_html, "Deprecated Digital Faculty ID still in sidebar"
        print("✓ Sidebar structured into approved navigation groups without deprecated modules.")
        results["sidebar_navigation"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 2: Teacher Submissions (Preview & Success Feedback)
        # -------------------------------------------------------------
        print("\n--- TEST 2: Teacher Submissions ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-submissions.html")
        desktop_page.wait_for_load_state("networkidle")

        # Open submission preview modal
        rows = desktop_page.locator('#submissionsTableBody tr')
        assert rows.count() > 0, "No submissions rows found"
        preview_btn = rows.first.locator('button[data-ngis-icon="checkCircle"], button[data-ngis-icon="view"]').first
        preview_btn.click()
        desktop_page.wait_for_selector("#submissionPreviewModal", state="visible")
        student_name = desktop_page.locator("#subPreviewStudentName").inner_text()
        print(f"✓ Submission preview modal opened for: {student_name}")
        assert len(student_name) > 0

        # Close via close button
        desktop_page.click("#closeSubPreviewBtn")
        desktop_page.wait_for_selector("#submissionPreviewModal", state="hidden")
        print("✓ Submission preview modal closed.")

        # Test publishing grade triggers animated success modal
        desktop_page.locator('#drawerScoreInput').fill('92')
        desktop_page.locator('button:has-text("Save & Publish Mark")').click()
        desktop_page.wait_for_selector("#ngisOperationSuccessModal", state="visible")
        succ_title = desktop_page.locator("#ngisOperationSuccessModal h3").inner_text()
        print(f"✓ Grade publishing triggered success modal: '{succ_title}'")
        desktop_page.click("button:has-text('Dismiss')")
        desktop_page.wait_for_selector("#ngisOperationSuccessModal", state="hidden")

        results["teacher_submissions"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 3: Teacher Attendance (Search, Status Picker & Mobile)
        # -------------------------------------------------------------
        print("\n--- TEST 3: Teacher Attendance ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-attendance.html")
        desktop_page.wait_for_load_state("networkidle")

        # Initial spreadsheet rows
        att_rows = desktop_page.locator('#attendanceSpreadsheetBody tr')
        assert att_rows.count() > 0, "No spreadsheet rows rendered"
        print(f"✓ Initial spreadsheet rows: {att_rows.count()}")

        # Quick Status Picker popup
        status_btn = att_rows.first.locator('button').first
        status_btn.click()
        desktop_page.wait_for_selector("#attendanceStatusPopup", state="visible")
        print("✓ Quick Attendance Status Picker popup opened.")
        desktop_page.locator('#attendanceStatusPopup button:has-text("Absent")').click()
        desktop_page.wait_for_selector("#attendanceStatusPopup", state="hidden")
        print("✓ Selected status 'Absent' via 1-click picker.")

        # Search filter
        search_input = desktop_page.locator("#searchAttendanceStudent")
        assert search_input.is_visible(), "Student search input missing in Attendance"
        search_input.fill("Sophea")
        desktop_page.wait_for_timeout(300)
        filtered_rows = desktop_page.locator("#attendanceSpreadsheetBody tr").count()
        print(f"✓ Attendance student search filtered to {filtered_rows} rows.")
        assert filtered_rows >= 1, "Search filter returned 0 rows"
        search_input.fill("")

        # Mobile Responsiveness test (375px)
        mobile_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-attendance.html")
        mobile_page.wait_for_load_state("networkidle")
        scroll_w = mobile_page.evaluate("() => document.documentElement.scrollWidth")
        inner_w = mobile_page.evaluate("() => window.innerWidth")
        diff = max(0, scroll_w - inner_w)
        print(f"✓ Mobile Attendance view width: {inner_w}px, scrollWidth: {scroll_w}px, overflow: {diff}px.")
        assert diff <= 0, f"Horizontal overflow detected: {diff}px"

        results["teacher_attendance"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 4: Teacher Student Roster (Profile Modal & Cleanup)
        # -------------------------------------------------------------
        print("\n--- TEST 4: Teacher Student Roster ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-roster.html")
        desktop_page.wait_for_load_state("networkidle")

        roster_text = desktop_page.locator("body").inner_text()
        assert "Enroll Student" not in roster_text, "Enroll Student button still present"
        assert "Cambridge IGCSE" not in roster_text, "Cambridge IGCSE still present"
        assert "100% Capacity Reached" not in roster_text, "100% Capacity Reached still present"

        # Click student row to open profile
        student_rows = desktop_page.locator("#rosterTableBody tr")
        assert student_rows.count() > 0, "No roster rows found"
        student_rows.first.click()
        desktop_page.wait_for_selector("#studentDetailModal", state="visible")
        detail_name = desktop_page.locator("#modalStudentName").inner_text()
        print(f"✓ Clicked student row opened Student Profile modal: '{detail_name}'")

        # Close detail modal
        desktop_page.click("#studentDetailModal button[onclick*='closeStudentModal']")
        desktop_page.wait_for_selector("#studentDetailModal", state="hidden")
        body_overflow = desktop_page.evaluate("() => document.body.style.overflow")
        assert body_overflow == "" or body_overflow == "visible"
        print("✓ Closed student profile modal and restored body scroll.")

        results["teacher_roster"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 5: Teacher Academic Reports (Pagination & Sync)
        # -------------------------------------------------------------
        print("\n--- TEST 5: Teacher Academic Reports ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-reports.html")
        desktop_page.wait_for_load_state("networkidle")

        summary_el = desktop_page.locator("#reportsPaginationSummary")
        assert summary_el.is_visible(), "Pagination summary missing"
        print(f"✓ Reports pagination summary: '{summary_el.inner_text()}'")

        # Check rows <= 8 per page
        page_rows = desktop_page.locator("#reportsTableBody tr")
        print(f"✓ Rows rendered on page 1: {page_rows.count()} (<= 8).")
        assert page_rows.count() <= 8

        # Test row selection sync
        first_report_row = page_rows.first
        first_report_row.click()
        assert "selected-row" in (first_report_row.get_attribute("class") or "")
        print("✓ Report row click highlights row with green border.")

        results["teacher_reports"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 6: Teacher Lessons (Multi-file, X button & Success)
        # -------------------------------------------------------------
        print("\n--- TEST 6: Teacher Lessons ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-lessons.html")
        desktop_page.wait_for_load_state("networkidle")

        desktop_page.click("button:has-text('Upload Lesson')")
        desktop_page.wait_for_selector("#uploadModal", state="visible")
        assert desktop_page.locator("#attachedFilesList").is_visible(), "Multi-file list missing"

        # Close via X button
        desktop_page.click("#closeUploadBtn")
        desktop_page.wait_for_selector("#uploadModal", state="hidden")
        print("✓ Lesson upload modal closed via X button.")

        # Reopen and submit
        desktop_page.click("button:has-text('Upload Lesson')")
        desktop_page.wait_for_selector("#uploadModal", state="visible")
        desktop_page.fill("#inputLessonTitle", "Thermodynamics & Heat Transfer")
        desktop_page.click("button[type='submit']")

        desktop_page.wait_for_selector("#ngisOperationSuccessModal", state="visible")
        print("✓ Lesson submission triggered animated success modal.")
        desktop_page.click("button:has-text('Dismiss')")
        desktop_page.wait_for_selector("#ngisOperationSuccessModal", state="hidden")

        results["teacher_lessons"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 7: Teacher Examinations & Quiz Notices
        # -------------------------------------------------------------
        print("\n--- TEST 7: Teacher Examinations & Quiz Notices ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-exams.html")
        desktop_page.wait_for_load_state("networkidle")

        title = desktop_page.locator("h1").first.inner_text()
        assert "Examination & Quiz Notices" in title
        create_btn = desktop_page.locator("button:has-text('Create Notice')")
        assert create_btn.is_visible()
        create_btn.click()
        desktop_page.wait_for_selector(".exw-modal-scrim.show", state="visible")
        print("✓ Create Notice modal opened.")
        desktop_page.click("button[data-action='close-modal']")
        desktop_page.wait_for_selector(".exw-modal-scrim.show", state="hidden")
        print("✓ Create Notice modal closed.")

        results["teacher_exams"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 8: Teacher Services & Lost-Found
        # -------------------------------------------------------------
        print("\n--- TEST 8: Teacher Services & Lost-Found ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-services.html")
        desktop_page.wait_for_load_state("networkidle")
        desktop_page.locator("button:has-text('New Request'):visible").first.click()
        desktop_page.wait_for_selector("#newRequestModal.show", state="visible")
        print("✓ Faculty Services New Request modal opened.")
        desktop_page.click("#newRequestModal button[onclick*='closeNewRequestModal']")
        desktop_page.wait_for_selector("#newRequestModal.show", state="hidden")
        print("✓ Faculty Services New Request modal closed.")

        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-lost-found.html")
        desktop_page.wait_for_load_state("networkidle")
        desktop_page.locator("button:has-text('Report Item'):visible").first.click()
        desktop_page.wait_for_selector("#reportModal.show", state="visible")
        print("✓ Teacher Lost & Found report modal opened.")
        desktop_page.click("#reportModal button[onclick*='closeReportModal']")
        desktop_page.wait_for_selector("#reportModal.show", state="hidden")
        print("✓ Teacher Lost & Found report modal closed.")

        results["teacher_services_lf"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 9: Deprecated Pages Safe Redirects
        # -------------------------------------------------------------
        print("\n--- TEST 9: Deprecated Pages Safe Redirects ---")
        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-departments.html")
        desktop_page.wait_for_url("**/teacher.html")
        print(f"✓ teacher-departments.html safely redirected to {desktop_page.url}")

        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-gradebook.html")
        desktop_page.wait_for_url("**/teacher-reports.html")
        print(f"✓ teacher-gradebook.html safely redirected to {desktop_page.url}")

        desktop_page.goto("http://127.0.0.1:3000/pages/teacher/teacher-documents.html")
        desktop_page.wait_for_url("**/teacher-lessons.html")
        print(f"✓ teacher-documents.html safely redirected to {desktop_page.url}")

        results["deprecated_redirects"] = "PASSED"

        # -------------------------------------------------------------
        # TEST 10: Mandatory Mobile Hamburger Menu on Mobile
        # -------------------------------------------------------------
        print("\n--- TEST 10: Mobile Hamburger Menu ---")
        mobile_page.goto("http://127.0.0.1:3000/pages/teacher/teacher.html")
        mobile_page.wait_for_load_state("networkidle")
        hamburger = mobile_page.locator("button[data-action='toggle-sidebar']:visible, .hamburger-btn:visible").first
        assert hamburger.is_visible(), "Mandatory hamburger menu button missing on mobile"
        print("✓ Mandatory mobile hamburger menu button verified.")
        results["mobile_hamburger"] = "PASSED"

        browser.close()
        print("\n==================================================")
        print("ALL 10 TEACHER PORTAL MASTER TESTS PASSED SUCCESSFULLY!")
        print("==================================================")
        for k, v in results.items():
            print(f"  {k}: {v}")

if __name__ == '__main__':
    run_teacher_portal_master_audit()
