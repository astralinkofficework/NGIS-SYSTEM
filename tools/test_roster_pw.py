from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-roster.html', wait_until='networkidle')
    page.wait_for_timeout(600)

    # 1. Assert removed features are NOT in the page
    content = page.content()
    assert "Enroll Student" not in content, "Enroll Student button still present"
    assert "Cambridge IGCSE" not in content, "Cambridge IGCSE still present"
    assert "100% capacity reached" not in content, "100% capacity reached still present"
    assert "Send Class Notice" not in content, "Send Class Notice button still present"

    # 2. Check table rows
    rows = page.locator('#rosterTableBody tr')
    count = rows.count()
    print('Roster table rows:', count)
    assert count >= 1, "Roster table is empty"

    # 3. Click first student row to open Student Profile
    rows.first.click()
    page.wait_for_timeout(400)

    modal = page.locator('#studentDetailModal')
    print('Student Profile modal visible:', modal.is_visible())
    assert modal.is_visible(), "Student Profile modal did not open on row click"

    s_name = page.locator('#modalStudentName').inner_text()
    s_id = page.locator('#modalStudentId').inner_text()
    print(f'Student Profile: {s_name} ({s_id})')
    assert len(s_name) > 0, "Student name empty in profile modal"

    # 4. Test X close button
    page.locator('#studentDetailModal button[onclick*="closeStudentModal"]').click()
    page.wait_for_timeout(300)
    print('After X close, modal visible:', modal.is_visible())
    assert not modal.is_visible(), "Student Profile modal did not close"

    # 5. Test search filter with #rosterSearchInput
    search_inp = page.locator('#rosterSearchInput')
    search_inp.fill('Bormey')
    page.wait_for_timeout(400)
    filtered = page.locator('#rosterTableBody tr').count()
    print('Filtered rows for "Bormey":', filtered)
    assert filtered >= 1, "Search filter returned 0 rows"

    browser.close()
    print("ALL ROSTER TESTS PASSED!")
