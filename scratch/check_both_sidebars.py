import os
import sys
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1400, "height": 1000})
    
    # 1. Admin
    page.goto('http://127.0.0.1:3000/pages/admin/admin.html')
    page.wait_for_selector('.sidebar')
    
    # Check if Teachers Management and Student Management exist
    t_mgmt = page.locator('button.nav-subgroup-label:has-text("Teachers Management")')
    s_mgmt = page.locator('button.nav-subgroup-label:has-text("Student Management")')
    print('Admin Teachers Management count:', t_mgmt.count())
    print('Admin Student Management count:', s_mgmt.count())
    
    # Click to expand if not already expanded
    if t_mgmt.count() > 0:
        parent_t = page.locator('.nav-subgroup[data-subgroup-id="teachers-mgmt-drop"]')
        if 'expanded' not in parent_t.get_attribute('class'):
            t_mgmt.first.click()
            page.wait_for_timeout(300)
            
    if s_mgmt.count() > 0:
        parent_s = page.locator('.nav-subgroup[data-subgroup-id="student-mgmt-drop"]')
        if 'expanded' not in parent_s.get_attribute('class'):
            s_mgmt.first.click()
            page.wait_for_timeout(300)
            
    acad = page.locator('button.nav-nested-label:has-text("Academic Result")')
    print('Admin Academic Result count:', acad.count())
    if acad.count() > 0:
        parent_a = page.locator('.nav-nested-group[data-nested-id="academic-result-drop"]')
        if 'expanded' not in parent_a.get_attribute('class'):
            acad.first.click()
            page.wait_for_timeout(300)
            
    sidebar = page.locator('#sidebar')
    sidebar.screenshot(path='scratch/both_sidebars_admin.png')
    print('Admin screenshot saved to scratch/both_sidebars_admin.png')
    
    # 2. Principal
    page.goto('http://127.0.0.1:3000/pages/principal/principal.html')
    page.wait_for_selector('.sidebar')
    
    t_mgmt = page.locator('button.nav-subgroup-label:has-text("Teachers Management")')
    s_mgmt = page.locator('button.nav-subgroup-label:has-text("Student Management")')
    print('Principal Teachers Management count:', t_mgmt.count())
    print('Principal Student Management count:', s_mgmt.count())
    
    if t_mgmt.count() > 0:
        parent_t = page.locator('.nav-subgroup[data-subgroup-id="teachers-mgmt-drop"]')
        if 'expanded' not in parent_t.get_attribute('class'):
            t_mgmt.first.click()
            page.wait_for_timeout(300)
            
    if s_mgmt.count() > 0:
        parent_s = page.locator('.nav-subgroup[data-subgroup-id="student-mgmt-drop"]')
        if 'expanded' not in parent_s.get_attribute('class'):
            s_mgmt.first.click()
            page.wait_for_timeout(300)
            
    acad = page.locator('button.nav-nested-label:has-text("Academic Result")')
    print('Principal Academic Result count:', acad.count())
    if acad.count() > 0:
        parent_a = page.locator('.nav-nested-group[data-nested-id="academic-result-drop"]')
        if 'expanded' not in parent_a.get_attribute('class'):
            acad.first.click()
            page.wait_for_timeout(300)
            
    sidebar = page.locator('#sidebar')
    sidebar.screenshot(path='scratch/both_sidebars_principal.png')
    print('Principal screenshot saved to scratch/both_sidebars_principal.png')
    
    browser.close()

