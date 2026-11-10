from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1024, 'height': 768})
    page.goto('http://127.0.0.1:3000/pages/student/student.html', wait_until='networkidle')
    
    profile_html = page.evaluate('() => document.querySelector(".ov-profile").outerHTML')
    upcoming_html = page.evaluate('() => document.querySelector(".ov-upcoming").outerHTML')
    deadlines_html = page.evaluate('() => document.querySelector(".ov-deadlines").outerHTML')
    
    print('=== PROFILE HTML ===')
    print(profile_html)
    print('=== UPCOMING HTML ===')
    print(upcoming_html)
    print('=== DEADLINES HTML ===')
    print(deadlines_html)
    
    browser.close()

