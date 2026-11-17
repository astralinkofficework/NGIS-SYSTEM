from playwright.sync_api import sync_playwright

def test_attendance():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": 1280, "height": 800})
        page = context.new_page()

        console_errors = []
        page_errors = []
        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: page_errors.append(str(err)))

        # Test 1: Open with ?dept=english
        print("=== Test 1: http://127.0.0.1:3000/pages/student/student-attendance.html?dept=english ===")
        page.goto("http://127.0.0.1:3000/pages/student/student-attendance.html?dept=english")
        page.wait_for_load_state("networkidle")

        chip_visible = page.is_visible("#attDeptChip")
        print(f"  attDeptChip is visible: {chip_visible}")
        assert not chip_visible, "attDeptChip MUST NOT be visible when ?dept=english is opened!"

        page_text = page.inner_text("body")
        has_dept_filter_text = "Department filter" in page_text or "English [Clear]" in page_text
        print(f"  Page contains 'Department filter': {has_dept_filter_text}")
        assert not has_dept_filter_text, "Page must not contain 'Department filter' text!"

        rows = page.query_selector_all("#attendanceLogBody tr")
        print(f"  Number of subject rows: {len(rows)}")
        assert len(rows) >= 8, f"Expected full attendance view with at least 8 subject rows, got {len(rows)}"

        cols = page.query_selector_all("#attHead th")
        print(f"  Number of columns in header: {len(cols)}")
        assert len(cols) >= 15, f"Expected full column attendance view with at least 15 columns, got {len(cols)}"

        # Verify English and other subjects are present
        subjects_text = [r.inner_text().split('\t')[0].split('\n')[0].strip() for r in rows]
        print("  Subjects in table:", subjects_text)
        assert any("ENGLISH" in s.upper() for s in subjects_text), "English subject must be in table"
        assert any("CALCULUS" in s.upper() or "MATH" in s.upper() for s in subjects_text), "Math/Calculus must be in table"
        assert any("KHMER" in s.upper() for s in subjects_text), "Khmer must be in table"

        # Test 2: Toggle Show More / Show Less
        toggle_btn = page.query_selector("#attToggleCols")
        if toggle_btn and page.is_visible("#attToggleCols"):
            lbl_before = page.inner_text("#attToggleLabel")
            count_before = page.inner_text("#attColCount")
            print(f"  Toggle button label: {lbl_before}, Count: {count_before}")

        # Test 3: Standard URL without params
        print("\n=== Test 2: http://127.0.0.1:3000/pages/student/student-attendance.html ===")
        page.goto("http://127.0.0.1:3000/pages/student/student-attendance.html")
        page.wait_for_load_state("networkidle")

        chip_visible2 = page.is_visible("#attDeptChip")
        print(f"  attDeptChip is visible: {chip_visible2}")
        assert not chip_visible2, "attDeptChip MUST NOT be visible!"

        rows2 = page.query_selector_all("#attendanceLogBody tr")
        cols2 = page.query_selector_all("#attHead th")
        print(f"  Number of subject rows: {len(rows2)}, Number of columns: {len(cols2)}")
        assert len(rows2) == len(rows), "Row count should match between ?dept=english and standard view!"
        assert len(cols2) == len(cols), "Column count should match between ?dept=english and standard view!"

        page.screenshot(path="docs/att_dept_english_after.png")
        print("  Screenshot saved to docs/att_dept_english_after.png")

        print(f"\nConsole errors: {len(console_errors)}")
        print(f"Page errors: {len(page_errors)}")
        assert len(page_errors) == 0, f"Found page errors: {page_errors}"

        print("\n>>> ALL ATTENDANCE TESTS PASSED! <<<")
        browser.close()

if __name__ == "__main__":
    test_attendance()
