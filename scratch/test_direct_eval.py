from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    page.on("console", lambda msg: print(f"CONSOLE [{msg.type}]: {msg.text}"))
    page.on("pageerror", lambda err: print(f"PAGE ERROR: {err}"))

    page.goto("http://127.0.0.1:3000/pages-directory.html", wait_until="networkidle")
    print("Clicking viewTableBtn...")
    res = page.evaluate("""() => {
        try {
            document.getElementById('viewTableBtn').click();
            return {
                view: document.getElementById('pagesTableWrap').style.display,
                bodyRows: document.getElementById('pagesTableBody').children.length,
                inner: document.getElementById('pagesTableBody').innerHTML.slice(0, 200)
            };
        } catch(e) {
            return { error: e.message, stack: e.stack };
        }
    }""")
    print("Result:", res)

    # Now for student-lost-found.html:
    page.goto("http://127.0.0.1:3000/pages/student/student-lost-found.html", wait_until="networkidle")
    res_lf = page.evaluate("""() => {
        try {
            // Check allItems
            const count = (typeof allItems !== 'undefined') ? allItems.length : 'undefined';
            // call renderStaffTable
            if (typeof renderStaffTable === 'function') renderStaffTable();
            return {
                allItemsCount: count,
                bodyRows: document.getElementById('lfStaffTableBody').children.length,
                inner: document.getElementById('lfStaffTableBody').innerHTML.slice(0, 200)
            };
        } catch(e) {
            return { error: e.message, stack: e.stack };
        }
    }""")
    print("LF Result:", res_lf)

    browser.close()

