from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 390, "height": 844})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    table = page.locator("table").first
    table.scroll_into_view_if_needed()
    page.screenshot(path="scratch/timetable_box_mobile_scrolled.png")
    browser.close()

print("Captured scrolled mobile screenshot!")

