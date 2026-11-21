import sys
from playwright.sync_api import sync_playwright

def test_lessons():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("Navigating to teacher-lessons.html...")
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-lessons.html")
        page.wait_for_load_state("networkidle")

        # 1. Check title & table rendered
        assert page.locator("#lessonsTbody tr").count() > 0, "No lesson rows rendered"
        print(f"Lesson rows rendered: {page.locator('#lessonsTbody tr').count()}")

        # 2. Open upload modal
        page.click("button:has-text('Upload Lesson')")
        page.wait_for_selector("#uploadModal", state="visible")
        print("Upload modal opened.")

        # Check attached files initially
        assert page.locator("#attachedFilesList").is_visible(), "Attached files list not visible"
        chips_count = page.locator("#attachedFilesList > div").count()
        print(f"Initial attached files: {chips_count}")

        # 3. Test Close via X button
        page.click("#closeUploadBtn")
        page.wait_for_selector("#uploadModal", state="hidden")
        print("Closed via X button successfully.")

        # Verify body scroll restored
        body_overflow = page.evaluate("() => document.body.style.overflow")
        assert body_overflow == "" or body_overflow == "visible", f"Body overflow not restored: {body_overflow}"

        # 4. Reopen and test Cancel button
        page.click("button:has-text('Upload Lesson')")
        page.wait_for_selector("#uploadModal", state="visible")
        page.click("#cancelUploadBtn")
        page.wait_for_selector("#uploadModal", state="hidden")
        print("Closed via Cancel button successfully.")

        # 5. Reopen and test Backdrop click
        page.click("button:has-text('Upload Lesson')")
        page.wait_for_selector("#uploadModal", state="visible")
        # Click outer modal area (top left 10, 10)
        page.mouse.click(10, 10)
        page.wait_for_selector("#uploadModal", state="hidden")
        print("Closed via Backdrop click successfully.")

        # 6. Reopen and submit new lesson with multi-file
        page.click("button:has-text('Upload Lesson')")
        page.wait_for_selector("#uploadModal", state="visible")
        page.fill("#inputLessonTitle", "Advanced Electromagnetic Induction")
        page.click("button[type='submit']")

        # Check success modal appears
        page.wait_for_selector("#ngisOperationSuccessModal", state="visible")
        success_title = page.locator("#ngisOperationSuccessModal h3").inner_text()
        print(f"Success modal triggered with title: '{success_title}'")
        assert "Lesson" in success_title or "Published" in success_title

        # Check new lesson was prepended to the table
        first_row_title = page.locator("#lessonsTbody tr:first-child .font-headline-sm").first.inner_text()
        print(f"First row title: '{first_row_title}'")
        assert "Advanced Electromagnetic Induction" in first_row_title

        # 7. Check row click navigation target
        print("Checking lesson title link to shared lesson-details.html...")
        with page.expect_navigation():
            page.locator("#lessonsTbody tr:first-child .font-headline-sm").first.click()
        current_url = page.url
        print(f"Navigated URL: {current_url}")
        assert "lesson-details.html" in current_url and "portal=teacher" in current_url, f"Unexpected target URL: {current_url}"

        browser.close()
        if errors:
            print("Console Errors:", errors)
            sys.exit(1)
        print("ALL LESSON MANAGEMENT TESTS PASSED!")

if __name__ == '__main__':
    test_lessons()
