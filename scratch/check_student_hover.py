from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto('http://127.0.0.1:3000/pages/student/student.html')
    page.wait_for_load_state('networkidle')
    
    # Check .ov-profile, .ov-upcoming, .ov-deadlines
    for sel in ['.ov-profile', '.ov-upcoming', '.ov-deadlines', '.ov-inner-panel']:
        card = page.locator(sel).first
        if card.count() > 0:
            bg_before = card.evaluate('el => window.getComputedStyle(el).backgroundColor')
            card.hover()
            bg_hover = card.evaluate('el => window.getComputedStyle(el).backgroundColor')
            print(f'{sel} -> before: {bg_before}, on hover: {bg_hover}')
    
    browser.close()

