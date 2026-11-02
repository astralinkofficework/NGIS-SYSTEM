from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    
    # 1. Teacher classes card hover
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-10a')
    page.wait_for_load_state('networkidle')
    card = page.locator('.ws-card').first
    card.hover()
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/92720a74-07b3-40fa-91e3-a384311b91aa/card_hover_teacher_classes.png')
    
    # 2. Student dashboard card hover
    page.goto('http://127.0.0.1:3000/pages/student/student.html')
    page.wait_for_load_state('networkidle')
    card2 = page.locator('.ov-profile').first
    card2.hover()
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/92720a74-07b3-40fa-91e3-a384311b91aa/card_hover_student.png')

    # 3. Principal dashboard card hover
    page.goto('http://127.0.0.1:3000/pages/principal/principal.html')
    page.wait_for_load_state('networkidle')
    card3 = page.locator('.ov-profile').first
    card3.hover()
    page.screenshot(path='C:/Users/oudom/.gemini/antigravity/brain/92720a74-07b3-40fa-91e3-a384311b91aa/card_hover_principal.png')
    
    browser.close()
    print('Screenshots saved!')

