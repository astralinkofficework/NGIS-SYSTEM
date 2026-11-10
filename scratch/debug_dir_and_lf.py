from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 1. Test Directory
    page.goto("http://127.0.0.1:3000/pages-directory.html", wait_until="networkidle")
    print("Directory loaded")
    page.click("#viewTableBtn")
    page.wait_for_timeout(1000)
    btns = page.locator("#pagesTableBody .action-group .action-icon-btn")
    print("Directory table action-icon-btn count:", btns.count())
    svgs = page.locator("#pagesTableBody .action-group .action-icon-btn svg")
    print("Directory table SVGs count:", svgs.count())

    # 2. Test Lost & Found
    page.goto("http://127.0.0.1:3000/pages/student/student-lost-found.html", wait_until="networkidle")
    print("Lost & Found loaded")
    page.evaluate("() => { if(window.setMainTab) window.setMainTab('staff_mgmt'); }")
    page.wait_for_timeout(1000)
    btns_lf = page.locator("#lfStaffTableBody .action-group .action-icon-btn, #lfStaffTableBody .action-group .action-btn-pill")
    print("Lost & found staff table action buttons count:", btns_lf.count())
    svgs_lf = page.locator("#lfStaffTableBody .action-group svg")
    print("Lost & found staff table SVGs count:", svgs_lf.count())

    browser.close()

