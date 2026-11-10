import sys
from playwright.sync_api import sync_playwright

print('Starting visual verification...')
sys.stdout.flush()

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    
    # 1. Desktop 1440x900
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    page.screenshot(path='scratch/assignment_desktop_1440_new.png', full_page=True)
    
    h1 = page.locator('h1').inner_text()
    print('Desktop H1:', h1)
    
    has_page_div = page.locator('.page').count() > 0
    print('Has .page wrapper:', has_page_div)
    sys.stdout.flush()
    
    # 2. Tablet 768x1024
    page.set_viewport_size({'width': 768, 'height': 1024})
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_tablet_768_new.png', full_page=True)
    print('Tablet screenshot taken')
    sys.stdout.flush()
    
    # 3. Mobile 390x844
    page.set_viewport_size({'width': 390, 'height': 844})
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_mobile_390_new.png', full_page=True)
    print('Mobile screenshot taken')
    sys.stdout.flush()
    
    # Check mobile tabs BEFORE opening drawer
    cohort_tab = page.locator('[data-act="wizard-mobile-tab"][data-tab="cohorts"]')
    cohort_tab.click()
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_mobile_cohorts.png')
    print('Cohorts tab clicked and screenshot taken')
    sys.stdout.flush()
    
    faculty_tab = page.locator('[data-act="wizard-mobile-tab"][data-tab="faculty"]')
    faculty_tab.click()
    page.wait_for_timeout(300)
    page.screenshot(path='scratch/assignment_mobile_faculty.png')
    print('Faculty tab clicked and screenshot taken')
    sys.stdout.flush()
    
    matrix_tab = page.locator('[data-act="wizard-mobile-tab"][data-tab="matrix"]')
    matrix_tab.click()
    page.wait_for_timeout(300)
    print('Matrix tab clicked')
    sys.stdout.flush()
    
    # Check hamburger button
    hamburger = page.locator('[data-action="toggle-sidebar"]').first
    print('Mobile hamburger visible:', hamburger.is_visible())
    sys.stdout.flush()
    
    # Click hamburger
    hamburger.click()
    page.wait_for_timeout(400)
    page.screenshot(path='scratch/assignment_mobile_drawer_open.png')
    print('Drawer screenshot taken')
    sys.stdout.flush()
    
    browser.close()
    print('Visual test successfully completed!')
