from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/teacher/teacher-classes.html?classId=cls-10a')
    page.wait_for_load_state('networkidle')
    
    # Check card hover on ws-card
    card = page.locator('.ws-card').first
    if card.count() > 0:
        box = card.bounding_box()
        print('Card found:', box)
        card.hover()
        page.screenshot(path='scratch/teacher_classes_card_hover.png')
        print('Hover screenshot taken')
        
        # Check computed styles before and after hover
        icon_box = card.locator('.w-9.h-9')
        print('Icon bg on hover:', icon_box.evaluate('el => window.getComputedStyle(el).backgroundColor'))
        print('Card bg on hover:', card.evaluate('el => window.getComputedStyle(el).backgroundColor'))
        print('Card before pseudo:', card.evaluate('el => window.getComputedStyle(el, "::before").content'))
        print('Card after pseudo:', card.evaluate('el => window.getComputedStyle(el, "::after").content'))

    # Check student dashboard
    page.goto('http://127.0.0.1:3000/pages/student/student.html')
    page.wait_for_load_state('networkidle')
    card2 = page.locator('.ov-profile, .ov-upcoming, .ov-inner-panel').first
    if card2.count() > 0:
        card2.hover()
        page.screenshot(path='scratch/student_card_hover.png')
        print('Student card hover screenshot taken')
        print('Student card bg:', card2.evaluate('el => window.getComputedStyle(el).backgroundColor'))
        print('Student card shadow:', card2.evaluate('el => window.getComputedStyle(el).boxShadow'))
        print('Student card before:', card2.evaluate('el => window.getComputedStyle(el, "::before").content'))
        print('Student card after:', card2.evaluate('el => window.getComputedStyle(el, "::after").content'))

    browser.close()

