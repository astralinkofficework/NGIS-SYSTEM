from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-submissions.html', wait_until='networkidle')
    page.wait_for_timeout(500)

    # 1. Check table rows
    rows = page.locator('#submissionsTableBody tr')
    count = rows.count()
    print('Submissions table rows:', count)
    assert count > 0, "No submissions rows found"

    # 2. Click tick / preview button on first row
    preview_btn = rows.first.locator('button[data-ngis-icon="checkCircle"], button[data-ngis-icon="view"]').first
    preview_btn.click()
    page.wait_for_timeout(400)

    # Check modal is visible
    modal = page.locator('#submissionPreviewModal')
    print('Submission preview modal visible:', modal.is_visible())
    assert modal.is_visible(), "Submission preview modal failed to open"

    student_name = page.locator('#subPreviewStudentName').inner_text()
    print('Previewed student name:', student_name)
    assert len(student_name) > 0, "Student name empty in preview"

    # 3. Test X close button
    page.locator('#closeSubPreviewBtn').click()
    page.wait_for_timeout(300)
    print('After close, modal visible:', modal.is_visible())
    assert not modal.is_visible(), "Submission preview modal failed to close"

    # 4. Check selected row indicator on first row
    first_tr = rows.first
    classes = first_tr.get_attribute('class')
    print('First row classes:', classes)
    assert 'border-[#0F5132]' in classes or 'selected-row' in classes, "Selected row indicator missing"

    # 5. Test search filter
    search_input = page.locator('#searchStudent')
    search_input.fill('Sophea')
    page.wait_for_timeout(300)
    filtered_count = page.locator('#submissionsTableBody tr').count()
    print('Filtered rows for "Sophea":', filtered_count)
    assert filtered_count >= 1, "Search filter returned no rows"

    # Clear search
    search_input.fill('')
    page.wait_for_timeout(300)

    # 6. Test save evaluation success animation
    page.locator('#drawerScoreInput').fill('95')
    page.locator('button:has-text("Save & Publish Mark")').click()
    page.wait_for_timeout(400)
    success_modal = page.locator('#ngisOperationSuccessModal')
    print('Success feedback visible:', success_modal.is_visible())
    assert success_modal.is_visible(), "Success animation modal not shown on publish"

    browser.close()
    print("ALL SUBMISSION TESTS PASSED!")
