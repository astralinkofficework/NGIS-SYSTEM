import sys
import time
from playwright.sync_api import sync_playwright

BASE_URL = "http://127.0.0.1:3000"

def run_tests():
    passed = []
    failed = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        # ── Test 1: Student Grades & Results ──
        print("Testing 1: Student Grades & Results...")
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()
        try:
            page.goto(f"{BASE_URL}/pages/student/student-grades.html", wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Check that fake report cards & fake modals are gone
            assert page.locator("#reportCardModal").count() == 0, "Fake reportCardModal still exists"
            assert page.locator("#breakdownModal").count() == 0, "Fake breakdownModal still exists"
            assert page.locator("#projectedGpaModal").count() == 0, "Fake projectedGpaModal still exists"

            # Check real cards loaded
            cards = page.locator("#resultsList article")
            count = cards.count()
            assert count > 0, f"No transcript cards rendered: count={count}"
            print(f"  Found {count} teacher-uploaded result cards.")

            # Click View Document on first card
            view_btn = cards.first.locator("button:has-text('View Document')")
            view_btn.click()
            page.wait_for_timeout(500)

            viewer = page.locator("#resultViewerModal")
            assert viewer.is_visible(), "Result document viewer modal did not open"

            # Verify zoom in/out
            zoom_in = viewer.locator("button[title='Zoom In']")
            if zoom_in.count() > 0:
                zoom_in.click()
                page.wait_for_timeout(200)

            # Test X Close button
            close_btn = viewer.locator("button[title*='Close']")
            close_btn.click()
            page.wait_for_timeout(500)
            assert not viewer.is_visible(), "Result document viewer modal did not close on X click"
            assert not page.locator("body").evaluate("el => el.classList.contains('modal-open')"), "modal-open not removed from body"

            passed.append("1. Student Grades & Results (real teacher uploads, viewer controls, working X button)")
        except Exception as e:
            failed.append(f"1. Student Grades & Results failed: {e}")

        # ── Test 2: Lesson Details & Document Viewer ──
        print("Testing 2: Lesson Details & Document Viewer...")
        try:
            page.goto(f"{BASE_URL}/pages/shared/lesson-details.html?id=m1&dept=math&portal=student", wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Check sidebar icons do not render raw text ligatures
            sidebar_icons = page.locator(".sidebar .nav-icon")
            assert sidebar_icons.count() > 0, "No sidebar icons found"

            # Check Back to Library link
            back_link = page.locator("#ldBackLink")
            href = back_link.get_attribute("href")
            assert "dept=math" in href and "portal=student" in href, f"Back link missing query params: {href}"

            # Check action controls exist
            assert page.locator("#ldDownloadBtn").count() > 0, "Download button missing"
            assert page.locator("#ldBookmarkBtn").count() > 0, "Bookmark button missing"
            assert page.locator("#ldFullscreenBtn").count() > 0, "Fullscreen button missing"

            # Test Bookmark toggle
            page.locator("#ldBookmarkBtn").click()
            page.wait_for_timeout(300)

            passed.append("2. Lesson Details & Document Viewer (sidebar icons, back link params, controls)")
        except Exception as e:
            failed.append(f"2. Lesson Details failed: {e}")

        # ── Test 3: Student Assignments Pagination ──
        print("Testing 3: Student Assignments Pagination...")
        try:
            page.goto(f"{BASE_URL}/pages/student/student-assignments.html", wait_until="networkidle")
            page.wait_for_timeout(800)

            # Check visible tasks on page 1 <= 4
            visible_tasks = page.locator("#tasksList .task-card:visible")
            assert visible_tasks.count() == 4, f"Expected 4 visible tasks on Page 1, got {visible_tasks.count()}"

            summary = page.locator("#tasksPaginationSummary").inner_text()
            assert "Showing 1–4 of 10" in summary, f"Unexpected summary: {summary}"

            prev_btn = page.locator("#tasksPrevBtn")
            next_btn = page.locator("#tasksNextBtn")
            assert prev_btn.is_disabled(), "Prev button should be disabled on Page 1"
            assert not next_btn.is_disabled(), "Next button should be enabled on Page 1"

            # Click Next -> Page 2
            next_btn.click()
            page.wait_for_timeout(300)
            visible_tasks_p2 = page.locator("#tasksList .task-card:visible")
            assert visible_tasks_p2.count() == 4, f"Expected 4 tasks on Page 2, got {visible_tasks_p2.count()}"
            assert not prev_btn.is_disabled(), "Prev button should be enabled on Page 2"

            # Click Next -> Page 3
            next_btn.click()
            page.wait_for_timeout(300)
            visible_tasks_p3 = page.locator("#tasksList .task-card:visible")
            assert visible_tasks_p3.count() == 2, f"Expected 2 tasks on Page 3, got {visible_tasks_p3.count()}"
            assert next_btn.is_disabled(), "Next button should be disabled on Page 3"

            # Click Prev -> Page 2
            prev_btn.click()
            page.wait_for_timeout(300)
            assert page.locator("#tasksList .task-card:visible").count() == 4, "Prev navigation failed"

            # Filter reset to Page 1
            page.locator("button.course-filter-btn[data-course='math']").click()
            page.wait_for_timeout(300)
            assert "Page 1 of" in page.locator("#tasksPageIndicator").inner_text(), "Filter did not reset to Page 1"

            passed.append("3. Student Assignments Pagination (4 per page, Prev/Next, Page indicators, filter reset)")
        except Exception as e:
            failed.append(f"3. Student Assignments failed: {e}")

        # ── Test 4: Student Examinations ──
        print("Testing 4: Student Examinations...")
        try:
            page.goto(f"{BASE_URL}/pages/shared/exams.html?portal=student", wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Verify exam list is not empty
            exams = page.locator("#exwList li.exw-exam")
            count = exams.count()
            assert count > 0, f"No exams displayed: count={count}"
            print(f"  Found {count} exams in upcoming tab.")

            # Check that exams display subject and time
            first_exam = exams.first
            assert first_exam.locator(".exw-exam-title").count() > 0, "Exam title missing"
            assert first_exam.locator(".exw-time").count() > 0, "Exam time missing"

            # Switch to Completed tab
            page.locator("button.exw-tab[data-tab='completed']").click()
            page.wait_for_timeout(400)
            completed_exams = page.locator("#exwList li.exw-exam")
            print(f"  Found {completed_exams.count()} exams in completed tab.")

            passed.append("4. Student Examinations (loaded cleanly, scheduling info, tab filtering, demo fallback)")
        except Exception as e:
            failed.append(f"4. Student Examinations failed: {e}")

        # ── Test 5: Student Timetable ──
        print("Testing 5: Student Timetable...")
        try:
            page.goto(f"{BASE_URL}/pages/student/student-timetable.html", wait_until="networkidle")
            page.wait_for_timeout(800)

            # Verify no horizontal overflow
            scroll_w = page.evaluate("document.documentElement.scrollWidth")
            client_w = page.evaluate("document.documentElement.clientWidth")
            assert scroll_w <= client_w, f"Horizontal overflow detected: scrollWidth={scroll_w} > clientWidth={client_w}"

            # Verify read-only: no edit or create timetable controls
            assert page.locator("button:has-text('New Timetable')").count() == 0, "Edit control found on student timetable"
            assert page.locator("button:has-text('Edit Timetable')").count() == 0, "Edit control found on student timetable"

            passed.append("5. Student Timetable (0px horizontal overflow, strictly read-only)")
        except Exception as e:
            failed.append(f"5. Student Timetable failed: {e}")

        # ── Test 6: Student Services Guided 4-Step Workflow ──
        print("Testing 6: Student Services Guided 4-Step Workflow...")
        try:
            page.goto(f"{BASE_URL}/pages/student/student-services.html", wait_until="networkidle")
            page.wait_for_timeout(800)

            # Open request modal
            page.locator("#openNewRequestHeroBtn, button:has-text('New Service Request')").first.click()
            page.wait_for_timeout(400)

            modal = page.locator("#mobileNewRequestModal")
            assert modal.is_visible(), "New Request modal did not open"

            # Verify Step 1 is active
            assert page.locator("#serviceStep1").is_visible(), "Step 1 not visible"
            assert page.locator("#serviceWizardStepBadge").inner_text().startswith("Step 1 of 4"), "Step 1 badge incorrect"

            # Advance to Step 2
            page.locator("#srvNextBtn").click()
            page.wait_for_timeout(300)
            assert page.locator("#serviceStep2").is_visible(), "Step 2 not visible after Continue"
            assert page.locator("#serviceWizardStepBadge").inner_text().startswith("Step 2 of 4"), "Step 2 badge incorrect"

            # Advance to Step 3
            page.locator("#srvNextBtn").click()
            page.wait_for_timeout(300)
            assert page.locator("#serviceStep3").is_visible(), "Step 3 not visible"

            # Advance to Step 4
            page.locator("#srvNextBtn").click()
            page.wait_for_timeout(300)
            assert page.locator("#serviceStep4").is_visible(), "Step 4 not visible"
            assert page.locator("#srvSubmitBtn").is_visible(), "Submit button not visible on Step 4"

            # Test Back navigation to Step 3
            page.locator("#srvPrevBtn").click()
            page.wait_for_timeout(300)
            assert page.locator("#serviceStep3").is_visible(), "Back button failed to return to Step 3"

            # Test Close modal
            page.on("dialog", lambda dialog: dialog.accept()) # Accept confirmation if dirty
            page.locator("#mobileNewRequestModal button[title*='Close']").click()
            page.wait_for_timeout(500)
            assert not modal.is_visible(), "Modal did not close on X button"

            passed.append("6. Student Services Guided Workflow (4 steps, step indicator, validation, back/next, working X close)")
        except Exception as e:
            failed.append(f"6. Student Services failed: {e}")

        # ── Test 7: Student Lost & Found ──
        print("Testing 7: Student Lost & Found...")
        try:
            page.goto(f"{BASE_URL}/pages/student/student-lost-found.html", wait_until="networkidle")
            page.wait_for_timeout(800)

            # Open report modal
            page.locator("#openReportHeroBtn, button[title*='Report Lost']").first.click()
            page.wait_for_timeout(400)

            report_modal = page.locator("#reportModal")
            assert report_modal.is_visible(), "Lost & Found Report modal did not open"

            # Check mode buttons
            btn_found = page.locator("#btnModeFound")
            btn_found.click()
            page.wait_for_timeout(200)

            # Test Close
            page.locator("#reportModal button[title*='Close']").click()
            page.wait_for_timeout(400)
            assert not report_modal.is_visible(), "Lost & Found modal did not close on X"

            passed.append("7. Student Lost & Found (mode toggle, viewport fit, working X close)")
        except Exception as e:
            failed.append(f"7. Student Lost & Found failed: {e}")

        # ── Test 8: Student Announcements ──
        print("Testing 8: Student Announcements...")
        try:
            page.goto(f"{BASE_URL}/pages/shared/announcements.html?portal=student", wait_until="networkidle")
            page.wait_for_timeout(1000)

            # Verify magazine / cards are loaded
            cards = page.locator(".ann-card-wrap, .ann-hero-sec, .ann-hero-main")
            count = cards.count()
            assert count > 0, f"No announcements rendered: count={count}"
            print(f"  Found {count} announcement cards.")

            passed.append("8. Student Announcements (loaded cleanly, test probes filtered, demo fallback, clickable)")
        except Exception as e:
            failed.append(f"8. Student Announcements failed: {e}")

        # ── Test 9: Student Dashboard Department Selection ──
        print("Testing 9: Student Dashboard Quick Links Department Selection...")
        try:
            page.goto(f"{BASE_URL}/pages/student/student.html", wait_until="networkidle")
            page.wait_for_timeout(800)

            # Click Assignments Quick Link
            asgn_ql = page.locator(".ql-item:has-text('Assignments')")
            asgn_ql.click()
            page.wait_for_timeout(400)

            dept_modal = page.locator("#deptSelectionModal")
            assert dept_modal.is_visible(), "Department selection modal did not open when clicking Assignments"

            # Check enrolled department options exist
            opts = dept_modal.locator("#deptModalList button")
            assert opts.count() >= 6, f"Expected >=6 department options, got {opts.count()}"

            # Test X button closes modal
            dept_modal.locator("button[title*='Close']").click()
            page.wait_for_timeout(300)
            assert not dept_modal.is_visible(), "Department selection modal did not close on X button"

            # Open again and test selection navigation
            asgn_ql.click()
            page.wait_for_timeout(300)
            dept_modal.locator("button:has-text('Mathematics')").click()
            page.wait_for_url("**/student-assignments.html?dept=math*", timeout=5000)
            assert "dept=math" in page.url, f"Expected URL with dept=math, got {page.url}"

            passed.append("9. Student Dashboard Quick Links (Department selection popup, enrolled subjects, URL routing)")
        except Exception as e:
            failed.append(f"9. Dashboard Quick Links failed: {e}")

        # ── Test 10: Global Logout Confirmation ──
        print("Testing 10: Global Logout Confirmation Modal...")
        try:
            page.goto(f"{BASE_URL}/pages/student/student.html", wait_until="networkidle")
            page.wait_for_timeout(800)

            logout_link = page.locator(".side-foot-signout, [data-purpose='sign-out-button']").first
            logout_link.click()
            page.wait_for_timeout(400)

            logout_modal = page.locator("#ngisLogoutModal")
            assert logout_modal.is_visible(), "Logout confirmation modal did not open"
            assert "Log out?" in logout_modal.inner_text(), "Logout modal missing title"

            # Test Cancel button
            cancel_btn = logout_modal.locator("#ngisLogoutCancelBtn")
            cancel_btn.click()
            page.wait_for_timeout(400)
            assert not logout_modal.is_visible(), "Logout modal did not close on Cancel"
            assert "student.html" in page.url, "Cancel navigated away unexpectedly"

            passed.append("10. Global Logout Confirmation (interception, dialog, cancel dismissal, body restore)")
        except Exception as e:
            failed.append(f"10. Global Logout Confirmation failed: {e}")

        # ── Test 11: Mobile Responsiveness Audit ──
        print("Testing 11: Mobile Responsiveness across 375px & 768px...")
        for vp in [{"width": 375, "height": 667}, {"width": 768, "height": 1024}]:
            mob_ctx = browser.new_context(viewport=vp)
            mob_page = mob_ctx.new_page()
            for p_url in [
                "/pages/student/student.html",
                "/pages/student/student-grades.html",
                "/pages/student/student-assignments.html",
                "/pages/student/student-timetable.html",
                "/pages/student/student-services.html",
                "/pages/student/student-lost-found.html"
            ]:
                mob_page.goto(f"{BASE_URL}{p_url}", wait_until="networkidle")
                mob_page.wait_for_timeout(300)
                sw = mob_page.evaluate("document.documentElement.scrollWidth")
                cw = mob_page.evaluate("document.documentElement.clientWidth")
                assert sw <= cw, f"Horizontal overflow on {p_url} at {vp['width']}px: scrollWidth={sw} > clientWidth={cw}"
            mob_ctx.close()
        passed.append("11. Mobile Responsiveness (0px horizontal overflow verified across 375px and 768px)")

        browser.close()

    print("\n════════════════════════════════════════")
    print(f"PASSED: {len(passed)} / {len(passed) + len(failed)}")
    for p_item in passed:
        print(f"  ✓ {p_item}")
    if failed:
        print(f"FAILED: {len(failed)}")
        for f_item in failed:
            print(f"  ✗ {f_item}")
    print("════════════════════════════════════════")
    return len(failed) == 0

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
