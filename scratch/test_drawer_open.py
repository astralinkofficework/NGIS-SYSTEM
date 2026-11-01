from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 850})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    sidebar = page.locator('#sidebar')
    print('Before click, sidebar has class open?', 'open' in (sidebar.get_attribute('class') or ''))
    
    # Click hamburger
    page.locator('#htbHamburger').click()
    page.wait_for_timeout(300)
    
    print('After click, sidebar has class open?', 'open' in (sidebar.get_attribute('class') or ''))
    print('Sidebar is visible?', sidebar.is_visible())
    
    page.screenshot(path='scratch/student_drawer_open.png')
    print('Saved drawer screenshot')
    
    browser.close()
    print('Check complete!')

