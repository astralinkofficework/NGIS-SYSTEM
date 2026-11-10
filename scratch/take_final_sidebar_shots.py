from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 1100})
    
    # 1. Admin Portal with both expanded
    page.goto('http://127.0.0.1:3000/pages/admin/admin-student-verify.html')
    page.wait_for_selector('#sidebar')
    page.wait_for_timeout(600)
    
    # Also expand Teachers Management to show both matching the user's screenshots
    t_btn = page.locator('button.nav-subgroup-label:has-text("Teachers Management")')
    parent_t = page.locator('.nav-subgroup[data-subgroup-id="teachers-mgmt-drop"]')
    if t_btn.count() > 0 and 'expanded' not in (parent_t.get_attribute('class') or ''):
        t_btn.first.click()
        page.wait_for_timeout(300)
        
    # Also expand Academic Result
    acad_btn = page.locator('button.nav-nested-label:has-text("Academic Result")')
    parent_a = page.locator('.nav-nested-group[data-nested-id="academic-result-drop"]')
    if acad_btn.count() > 0 and 'expanded' not in (parent_a.get_attribute('class') or ''):
        acad_btn.first.click()
        page.wait_for_timeout(300)
        
    sidebar = page.locator('#sidebar')
    sidebar.screenshot(path='scratch/admin_sidebar_both_expanded.png')
    
    # 2. Principal Portal with both expanded
    page.goto('http://127.0.0.1:3000/pages/principal/principal-student-verify.html')
    page.wait_for_selector('#sidebar')
    page.wait_for_timeout(600)
    
    t_btn = page.locator('button.nav-subgroup-label:has-text("Teachers Management")')
    parent_t = page.locator('.nav-subgroup[data-subgroup-id="teachers-mgmt-drop"]')
    if t_btn.count() > 0 and 'expanded' not in (parent_t.get_attribute('class') or ''):
        t_btn.first.click()
        page.wait_for_timeout(300)
        
    acad_btn = page.locator('button.nav-nested-label:has-text("Academic Result")')
    parent_a = page.locator('.nav-nested-group[data-nested-id="academic-result-drop"]')
    if acad_btn.count() > 0 and 'expanded' not in (parent_a.get_attribute('class') or ''):
        acad_btn.first.click()
        page.wait_for_timeout(300)
        
    sidebar = page.locator('#sidebar')
    sidebar.screenshot(path='scratch/principal_sidebar_both_expanded.png')
    
    browser.close()
    print("Screenshots taken successfully!")

