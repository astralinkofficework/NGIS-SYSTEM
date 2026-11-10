from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    errors = []
    page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

    # Test Directory
    page.goto("http://127.0.0.1:3000/pages-directory.html", wait_until="networkidle")
    print("Has #viewTableBtn?", page.locator("#viewTableBtn").count())
    page.click("#viewTableBtn")
    page.wait_for_timeout(500)
    print("Table HTML snippet:", page.locator("#pagesTableBody").inner_html()[:300])

    # Test Lost & Found
    page.goto("http://127.0.0.1:3000/pages/student/student-lost-found.html", wait_until="networkidle")
    print("Has #lfStaffTableBody?", page.locator("#lfStaffTableBody").count())
    res = page.evaluate("() => { if(window.setMainTab) window.setMainTab('staff_mgmt'); return typeof window.renderStaffTable; }")
    print("renderStaffTable type:", res)
    page.wait_for_timeout(500)
    print("Staff Table HTML snippet:", page.locator("#lfStaffTableBody").inner_html()[:300])

    browser.close()

