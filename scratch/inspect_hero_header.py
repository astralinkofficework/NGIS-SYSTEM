from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    
    hero_html = page.evaluate("() => document.querySelector('header.hero')?.outerHTML")
    print('Hero header length:', len(hero_html) if hero_html else 0)
    print(hero_html[:1500])
    browser.close()

