from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:3000/pages/admin/admin-timetables.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    page.screenshot(path='scratch/verify_admin_timetables_mobile.png')
    browser.close()

