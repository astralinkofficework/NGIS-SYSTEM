from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", wait_until="networkidle")
    page.wait_for_selector("#ks-root .ks-timetable-grid", timeout=10000)
    page.screenshot(path="scratch/principal_builder_desktop_1440.png")
    print("Principal Timetable Builder loaded and screenshot saved!")
    browser.close()

