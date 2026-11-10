from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 900})
    page.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", wait_until="networkidle")
    page.wait_for_timeout(1000)
    page.screenshot(path="scratch/timetable_box_desktop.png")
    
    # Also mobile
    page_m = browser.new_page(viewport={"width": 390, "height": 844})
    page_m.goto("http://127.0.0.1:3000/pages/principal/principal-timetable-builder.html", wait_until="networkidle")
    page_m.wait_for_timeout(1000)
    page_m.screenshot(path="scratch/timetable_box_mobile.png")
    
    browser.close()

print("Captured timetable box screenshots!")

