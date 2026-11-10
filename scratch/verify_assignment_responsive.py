from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Desktop 1440x900
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='scratch/assignment_desktop_1440_new.png', full_page=True)
    
    h1 = page.locator('h1').inner_text()
    print('Desktop H1:', h1)
    
    # Check page wrapper
    has_page_div = page.locator('.page').count() > 0
    print('Has .page wrapper:', has_page_div)
    
    # 2. Tablet 768x1024
    page.set_viewport_size({'width': 768, 'height': 1024})
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_tablet_768_new.png', full_page=True)
    print('Tablet screenshot taken')
    
    # 3. Mobile 390x844
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_mobile_390_new.png', full_page=True)
    
    # Check hamburger button
    hamburger = page.locator('header.lg\\:hidden [data-action="toggle-sidebar"]')
    print('Mobile hamburger count:', hamburger.count())
    print('Mobile hamburger visible:', hamburger.is_visible())
    
    # Click hamburger button to test opening drawer
    hamburger.click()
    page.wait_for_timeout(400)
    page.screenshot(path='scratch/assignment_mobile_drawer_open.png')
    
    sidebar_active = page.evaluate("() => document.getElementById('sidebar')?.classList.contains('active') || document.querySelector('aside')?.classList.contains('open') || document.querySelector('.sidebar')?.classList.contains('open') || document.querySelector('.sidebar-overlay')?.classList.contains('active')")
    print('Sidebar opened:', sidebar_active)
    
    # Check mobile tabs switching
    cohort_tab = page.locator('[data-act="wizard-mobile-tab"][data-tab="cohorts"]')
    cohort_tab.click()
    page.wait_for_timeout(300)
    cohort_visible = page.locator('#cohortCardsList').is_visible()
    print('Cohorts tab clicked, cohorts visible:', cohort_visible)
    
    # Click first cohort item to switch back to matrix
    first_cohort = page.locator('.cohort-item').first
    first_cohort.click()
    page.wait_for_timeout(300)
    matrix_visible = page.locator('table').is_visible()
    print('Cohort clicked, switched to matrix, table visible:', matrix_visible)
    
    browser.close()

