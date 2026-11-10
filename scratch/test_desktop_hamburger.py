from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1024, 'height': 768})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    hb = page.query_selector('#htbHamburger')
    if hb:
        print('Desktop hamburger found, box:', hb.bounding_box())
        hb.click()
        page.wait_for_timeout(400)
        sidebar = page.query_selector('#sidebar')
        if sidebar:
            print('Sidebar class on desktop click:', sidebar.get_attribute('class'))
            
    browser.close()
print('Desktop hamburger check done.')

