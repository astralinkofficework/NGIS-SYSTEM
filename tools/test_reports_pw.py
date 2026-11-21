from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-reports.html', wait_until='networkidle')
    page.wait_for_timeout(600)

    # 1. Check table rows count on page 1 (should be 8)
    rows = page.locator('#reportsTableBody tr')
    count = rows.count()
    print('Reports page 1 rows:', count)
    assert count == 8, f"Expected 8 rows on page 1, got {count}"

    # 2. Check pagination indicator
    summary = page.locator('#reportsPaginationSummary').inner_text()
    indicator = page.locator('#reportsPageIndicator').inner_text()
    print(f'Pagination info: {summary} | {indicator}')
    assert "Showing 1 to 8" in summary, "Pagination summary incorrect"
    assert "Page 1 of" in indicator, "Page indicator incorrect"

    # 3. Test Next button
    page.locator('#reportsNextBtn').click()
    page.wait_for_timeout(300)
    summary2 = page.locator('#reportsPaginationSummary').inner_text()
    indicator2 = page.locator('#reportsPageIndicator').inner_text()
    print(f'After Next: {summary2} | {indicator2}')
    assert "Showing 9 to 16" in summary2, "Next page summary incorrect"
    assert "Page 2 of" in indicator2, "Next page indicator incorrect"

    # 4. Click a row and check selected indicator
    page.locator('#reportsTableBody tr').first.click()
    page.wait_for_timeout(200)
    first_classes = page.locator('#reportsTableBody tr').first.get_attribute('class')
    print('Selected row classes:', first_classes)
    assert 'border-[#0F5132]' in first_classes or 'selected-row' in first_classes, "Selected row indicator missing"

    # 5. Open upload modal and check student context
    page.locator('button[onclick*="openUploadTranscriptModal"]').first.click()
    page.wait_for_timeout(300)
    upload_modal = page.locator('#modalUploadTranscript')
    print('Upload modal visible:', upload_modal.is_visible())
    assert upload_modal.is_visible(), "Upload modal did not open"

    # 6. Test X close button
    page.locator('#modalUploadTranscript button[aria-label="Close dialog"]').click()
    page.wait_for_timeout(300)
    print('After X close, upload modal visible:', upload_modal.is_visible())
    assert not upload_modal.is_visible(), "Upload modal failed to close"

    browser.close()
    print("ALL REPORTS TESTS PASSED!")
