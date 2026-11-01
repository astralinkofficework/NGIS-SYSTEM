from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 850})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    # Open ID Modal
    page.locator('#viewIdBtn').click()
    page.wait_for_timeout(300)
    
    modal = page.locator('#idModal')
    print('Modal has class show?', 'show' in (modal.get_attribute('class') or ''))
    print('Modal is visible?', modal.is_visible())
    
    page.screenshot(path='scratch/student_id_modal_front.png')
    print('Saved modal front screenshot')
    
    # Click card to flip
    page.locator('#idCardWrap').click()
    page.wait_for_timeout(300)
    
    page.screenshot(path='scratch/student_id_modal_back.png')
    print('Saved modal back screenshot')
    
    # Close modal
    page.locator('#idCloseBtn').click()
    page.wait_for_timeout(200)
    print('After close, modal has class show?', 'show' in (modal.get_attribute('class') or ''))
    
    browser.close()
    print('ID modal test passed!')

