from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/admin/admin-student-profiles.html', wait_until='networkidle')
    page.wait_for_timeout(1000)
    
    # Click view button
    page.locator('button[data-act="view"]').first.click()
    page.wait_for_timeout(1000)
    page.screenshot(path='student_profile_modal_live.png')
    print('Modal screenshot captured: student_profile_modal_live.png')

    # Also capture at 1024px (tablet landscape) and 375px (mobile)
    page.set_viewport_size({'width': 1024, 'height': 768})
    page.wait_for_timeout(500)
    page.screenshot(path='student_profile_modal_1024.png')
    
    page.set_viewport_size({'width': 375, 'height': 812})
    page.wait_for_timeout(500)
    page.screenshot(path='student_profile_modal_375.png')
    print('Captured at 1024 and 375.')

    browser.close()
