from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 390, 'height': 844})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    hb = page.query_selector('.student-mobile-view button[data-action="toggle-sidebar"]')
    if hb:
        hb.click()
        page.wait_for_timeout(400)
        sidebar = page.query_selector('#sidebar')
        if sidebar:
            print('Sidebar class:', sidebar.get_attribute('class'))
        scrim = page.query_selector('#scrim')
        if scrim:
            print('Scrim class:', scrim.get_attribute('class'))
            
    browser.close()
print('Drawer check done.')
