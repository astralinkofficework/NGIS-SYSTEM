from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1440, "height": 900})
    page.on("console", lambda msg: print(f"BROWSER CONSOLE [{msg.type}]: {msg.text}"))
    page.on("pageerror", lambda err: print(f"BROWSER ERROR: {err}"))
    page.goto("http://127.0.0.1:3000/pages/admin/admin-timetable-management.html", wait_until="networkidle")
    print("Page loaded, evaluating grid preview...")
    # Call previewClass directly
    page.evaluate("() => TIMETABLE_OVERSIGHT.previewClass('class_7B')")
    import time
    time.sleep(2)
    html = page.locator("#timetableGridPreview").inner_html()
    print("timetableGridPreview HTML:")
    print(html[:500])
    browser.close()

