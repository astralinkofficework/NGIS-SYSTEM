import sys
from playwright.sync_api import sync_playwright

def test_teacher_exams():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1280, "height": 900})

        errors = []
        page.on("pageerror", lambda err: errors.append(str(err)))

        print("Navigating to teacher-exams.html...")
        page.goto("http://127.0.0.1:3000/pages/teacher/teacher-exams.html")
        page.wait_for_load_state("networkidle")

        # 1. Verify title
        title_text = page.locator("h1").first.inner_text()
        print(f"Page title: {title_text}")
        assert "Examination & Quiz Notices" in title_text

        # 2. Check "Create Notice" button
        btn = page.locator("button:has-text('Create Notice')")
        assert btn.is_visible(), "Create Notice button not visible"
        print("Create Notice button is visible.")

        # 3. Open modal
        btn.click()
        page.wait_for_selector(".exw-modal-scrim.show", state="visible")
        modal_title = page.locator(".exw-modal-title").inner_text()
        print(f"Modal title: '{modal_title}'")
        assert "Notice" in modal_title or "Examination" in modal_title

        # Close modal via close button
        page.click("button[data-action='close-modal']")
        page.wait_for_selector(".exw-modal-scrim.show", state="hidden")
        print("Modal closed successfully.")

        # 4. Check table and row click
        rows = page.locator(".exw-table tbody tr")
        row_count = rows.count()
        print(f"Exams rows count: {row_count}")
        if row_count > 0:
            first_row = rows.first
            first_row.click()
            class_attr = first_row.get_attribute("class")
            print(f"First row class after click: {class_attr}")
            assert "selected-row" in class_attr, "selected-row not added on row click"

        browser.close()
        if errors:
            print("Console Errors:", errors)
            sys.exit(1)
        print("ALL TEACHER EXAMS TESTS PASSED!")

if __name__ == '__main__':
    test_teacher_exams()
