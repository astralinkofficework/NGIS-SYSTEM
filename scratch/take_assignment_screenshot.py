from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='scratch/assignment_desktop_1440.png', full_page=True)
    
    # mobile viewport
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(500)
    page.screenshot(path='scratch/assignment_mobile_390.png', full_page=True)
    
    print('Screenshots saved to scratch/assignment_desktop_1440.png and scratch/assignment_mobile_390.png')
    browser.close()

