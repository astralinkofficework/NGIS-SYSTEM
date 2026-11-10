from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-attendance.html')
    page.wait_for_selector('#arrival-oversight-table')
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/principal_attendance_clean.png')
    browser.close()

