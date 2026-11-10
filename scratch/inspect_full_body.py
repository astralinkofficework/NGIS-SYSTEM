from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={'width': 1440, 'height': 900})
    page.goto('http://127.0.0.1:3000/pages/principal/principal-teacher-class-assignment.html')
    page.wait_for_load_state('networkidle')
    
    html = page.evaluate("() => document.body.innerHTML")
    # find where heroBanner was or what replaced it
    print('heroBanner in body:', 'heroBanner' in html)
    print('first 1000 chars of body:')
    print(html[:1000])
    browser.close()

