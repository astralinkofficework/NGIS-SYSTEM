from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-attendance.html', wait_until='networkidle')
    page.wait_for_timeout(500)

    # 1. Check rows in spreadsheet
    rows = page.locator('#attendanceSpreadsheetBody tr')
    print('Initial spreadsheet rows:', rows.count())
    assert rows.count() > 0, "No spreadsheet rows rendered"

    # 2. Test status picker click on Day 0 of first row
    status_btn = rows.first.locator('button').first
    status_btn.click()
    page.wait_for_timeout(300)

    popup = page.locator('#attendanceStatusPopup')
    print('Status picker popup visible:', popup.is_visible())
    assert popup.is_visible(), "Quick status picker popup did not open"

    # 3. Select 'Absent' (A)
    page.locator('#attendanceStatusPopup button:has-text("Absent")').click()
    page.wait_for_timeout(300)
    print('After selecting status, popup visible:', popup.is_visible())
    assert not popup.is_visible(), "Popup should close after selection"

    # 4. Check search filter
    search_input = page.locator('#searchAttendanceStudent')
    search_input.fill('Sophea')
    page.wait_for_timeout(300)
    filtered_rows = page.locator('#attendanceSpreadsheetBody tr').count()
    print('Filtered rows for "Sophea":', filtered_rows)
    assert filtered_rows >= 1, "Search filter failed"

    # 5. Mobile responsive test at 375px
    page.set_viewport_size({'width': 375, 'height': 812})
    page.wait_for_timeout(300)
    scroll_w = page.evaluate('document.documentElement.scrollWidth')
    inner_w = page.evaluate('window.innerWidth')
    print(f'Mobile 375px: scrollWidth={scroll_w}, innerWidth={inner_w}')
    # Allow at most 0px difference outside of table horizontal scroll container
    diff = max(0, scroll_w - inner_w)
    print('Mobile horizontal overflow difference:', diff)
    assert diff <= 0, f"Detected {diff}px horizontal overflow on mobile!"

    browser.close()
    print("ALL ATTENDANCE TESTS PASSED!")
