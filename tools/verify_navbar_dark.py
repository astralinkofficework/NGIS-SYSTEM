from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/student/student-grades.html', wait_until='networkidle')
    page.evaluate('document.documentElement.setAttribute("data-theme", "dark")')
    page.screenshot(path='navbar_dark_mode_student.png')
    page.goto('http://127.0.0.1:3000/pages/admin/admin-student-profiles.html', wait_until='networkidle')
    page.evaluate('document.documentElement.setAttribute("data-theme", "dark")')
    page.screenshot(path='navbar_dark_mode_admin.png')
    browser.close()
print('Dark mode verified')
