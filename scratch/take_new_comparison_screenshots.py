from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(400)
    
    # Desktop full page
    page.screenshot(path='scratch/assignment_clean_borders_1440.png', full_page=True)
    
    # Specific crop matching the user's uploaded area (the 3 columns)
    cols = page.locator('.grid.grid-cols-1.xl\\:grid-cols-12')
    cols.screenshot(path='scratch/assignment_3_cols_crop.png')
    
    # Mobile view
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_clean_mobile_390.png', full_page=True)
    
    browser.close()
    print('Screenshots taken successfully!')

